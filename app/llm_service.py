import grpc
from concurrent import futures
import llm_pb2
import llm_pb2_grpc
from vllm import LLM, SamplingParams

class LLMService(llm_pb2_grpc.LLMServiceServicer):
    def __init__(self):
        self.model_path = "path/to/Hermes-3-Llama-3.1-70B-lorablated"
        self.llm = LLM(model=self.model_path)
        self.sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=2048)

    def GenerateCode(self, request, context):
        prompt = request.prompt
        outputs = self.llm.generate([prompt], self.sampling_params)
        generated_text = outputs[0].outputs[0].text

        files = self._parse_generated_text(generated_text)
        return llm_pb2.CodeResponse(files=[llm_pb2.File(name=name, content=content) for name, content in files.items()])

    def _parse_generated_text(self, generated_text):
        files = {}
        current_file = None
        current_content = []

        for line in generated_text.split('\n'):
            if line.startswith('## file:'):
                if current_file:
                    files[current_file] = '\n'.join(current_content)
                current_file = line[8:].strip()
                current_content = []
            else:
                current_content.append(line)

        if current_file:
            files[current_file] = '\n'.join(current_content)

        return files

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_pb2_grpc.add_LLMServiceServicer_to_server(LLMService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
