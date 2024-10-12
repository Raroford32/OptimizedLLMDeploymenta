use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use tonic::Request;

pub mod llm {
    tonic::include_proto!("llm");
}

use llm::{CodeRequest, LlmServiceClient};

#[derive(Serialize, Deserialize)]
struct GenerateRequest {
    prompt: String,
    project_name: String,
}

#[derive(Serialize)]
struct GenerateResponse {
    status: String,
    message: String,
    files: Vec<FileResponse>,
}

#[derive(Serialize)]
struct FileResponse {
    name: String,
    content: String,
}

async fn generate_code(req: web::Json<GenerateRequest>) -> impl Responder {
    let mut client = LlmServiceClient::connect("http://[::1]:50051")
        .await
        .expect("Failed to connect to LLM service");

    let request = Request::new(CodeRequest {
        prompt: req.prompt.clone(),
    });

    match client.generate_code(request).await {
        Ok(response) => {
            let files = response.into_inner().files;
            let file_responses: Vec<FileResponse> = files
                .into_iter()
                .map(|file| FileResponse {
                    name: file.name,
                    content: file.content,
                })
                .collect();

            let response = GenerateResponse {
                status: "success".to_string(),
                message: format!("Code generated for project: {}", req.project_name),
                files: file_responses,
            };
            HttpResponse::Ok().json(response)
        }
        Err(e) => {
            eprintln!("Error generating code: {:?}", e);
            HttpResponse::InternalServerError().json(GenerateResponse {
                status: "error".to_string(),
                message: "Failed to generate code".to_string(),
                files: vec![],
            })
        }
    }
}

async fn index() -> impl Responder {
    HttpResponse::Ok().body("Welcome to the Advanced Code Generator Chatbot!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Starting server at http://0.0.0.0:8080");
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            .route("/generate", web::post().to(generate_code))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
