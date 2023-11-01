# neuropulse
A GPU monitoring tool for NVIDIA GPUs. It is a simple tool that can be used to monitor the GPU usage and temperature of NVIDIA GPUs. It is written in Python and uses the [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) tool to get the GPU information. It can be used to monitor the GPU usage and temperature of multiple GPUs in a node or in a cluster (using a mongoDB database).

## Installation
The tool can be installed using pip:
```
pip install -r requirements.txt
```

## Usage

To run neuropulse on a node run the following command:
```bash
bash neuropulse --config config.yaml --node NODE_NAME
```
where `NODE_NAME` is the name of the node. The `config.yaml` file contains the configuration of the tool. The configuration file is a yaml file with the following structure:
```yaml
app_logging_level: INFO
gpu_monitoring_interval: 10
environment_name: dev
handlers:
  - type: file
    config:
      file_prefix: gpu_monitor
      rotate: 1000
      name: gpu_monitor
      gzip: true
  - type: console
    config:
      name: gpu_monitor
  - type: mongo
    config:
      mongo_host: 0.0.0.0
      mongo_db: gpu_monitor
      mongo_collection: gpu_monitor_0
```

- The `app_logging_level` is the logging level of the tool. 
- The `gpu_monitoring_interval` is the interval in seconds between each monitoring of the GPUs.
- The `environment_name` is the name of the environment. It is used to distinguish between different environments (e.g. dev, prod, etc.).
- The `handlers` is a list of handlers that are used to handle the GPU information. The handlers can be of type `file`, `console` or `mongo`. The `file` handler is used to write the GPU information to a file. The `console` handler is used to print the GPU information to the console. The `mongo` handler is used to write the GPU information to a mongoDB database. The `mongo_host` is the host of the mongoDB database. The `mongo_db` is the name of the mongoDB database. The `mongo_collection` is the name of the mongoDB collection. The `node_id` is the id of the node. It is used to distinguish between different nodes in the mongoDB database.
- The `file_prefix` is the prefix of the file that is used to write the GPU information. The `rotate` is the number of files to keep. The `name` is the name of the file. The `gzip` is a boolean that indicates whether to compress the file or not.
- The `name` is the name of the console handler.
- The `node_id` is the id of the node. It is used to distinguish between different nodes in the mongoDB database.
- The `mongo_host` is the host of the mongoDB database. The `mongo_db` is the name of the mongoDB database. 


To use neuropulse in a cluster you need to setup a mongoDB database. You can use the docker-compose file to setup a mongoDB database. Then in each node you need to run the following command:
```bash
bash neuropulse --config config.yaml --node NODE_NAME
```


## License
[MIT](https://choosealicense.com/licenses/mit/)


