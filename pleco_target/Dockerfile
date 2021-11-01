FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY pleco_target/ /service/pleco_target/
WORKDIR /service/pleco_target
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/pleco_target.proto

EXPOSE 50051
ENTRYPOINT [ "python", "pleco_target.py" ]