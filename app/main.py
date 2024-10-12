import os
from concurrent import futures
import grpc
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
import llm_pb2
import llm_pb2_grpc
from models import User, Project
from git_handler import create_git_repo, commit_changes

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# gRPC client for LLM service
llm_channel = grpc.insecure_channel('localhost:50051')
llm_stub = llm_pb2_grpc.LLMServiceStub(llm_channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json['prompt']
    project_name = request.json['project_name']
    
    # Generate code using the LLM service
    response = llm_stub.GenerateCode(llm_pb2.CodeRequest(prompt=prompt))
    generated_files = {file.name: file.content for file in response.files}
    
    # Create a new project in the database
    project = Project(name=project_name, user_id=session.get('user_id'))
    db.session.add(project)
    db.session.commit()
    
    # Create a Git repository for the project
    repo_path = create_git_repo(project_name)
    
    # Save generated files and commit changes
    for file_name, content in generated_files.items():
        file_path = os.path.join(repo_path, file_name)
        with open(file_path, 'w') as f:
            f.write(content)
    
    commit_changes(repo_path, "Initial commit")
    
    return jsonify({'status': 'success', 'message': 'Code generated and project created'})

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if User.query.filter_by(username=username).first():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'status': 'success', 'message': 'Logged in successfully'})
    
    return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
