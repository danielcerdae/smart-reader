# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
""" Utils to interact with the Triton Inference Server
"""

import typing
from urllib.parse import urlparse

import torch


class TritonRemoteModel:
<<<<<<< HEAD
    """A wrapper over a model served by the Triton Inference Server. It can
=======
    """ A wrapper over a model served by the Triton Inference Server. It can
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
    be configured to communicate over GRPC or HTTP. It accepts Torch Tensors
    as input and returns them as outputs.
    """

    def __init__(self, url: str):
        """
        Keyword arguments:
        url: Fully qualified address of the Triton server - for e.g. grpc://localhost:8000
        """

        parsed_url = urlparse(url)
        if parsed_url.scheme == "grpc":
            from tritonclient.grpc import InferenceServerClient, InferInput

            self.client = InferenceServerClient(parsed_url.netloc)  # Triton GRPC client
            model_repository = self.client.get_model_repository_index()
            self.model_name = model_repository.models[0].name
<<<<<<< HEAD
            self.metadata = self.client.get_model_metadata(
                self.model_name, as_json=True
            )

            def create_input_placeholders() -> typing.List[InferInput]:
                return [
                    InferInput(i["name"], [int(s) for s in i["shape"]], i["datatype"])
                    for i in self.metadata["inputs"]
                ]
=======
            self.metadata = self.client.get_model_metadata(self.model_name, as_json=True)

            def create_input_placeholders() -> typing.List[InferInput]:
                return [
                    InferInput(i['name'], [int(s) for s in i["shape"]], i['datatype']) for i in self.metadata['inputs']]
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1

        else:
            from tritonclient.http import InferenceServerClient, InferInput

            self.client = InferenceServerClient(parsed_url.netloc)  # Triton HTTP client
            model_repository = self.client.get_model_repository_index()
<<<<<<< HEAD
            self.model_name = model_repository[0]["name"]
=======
            self.model_name = model_repository[0]['name']
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
            self.metadata = self.client.get_model_metadata(self.model_name)

            def create_input_placeholders() -> typing.List[InferInput]:
                return [
<<<<<<< HEAD
                    InferInput(i["name"], [int(s) for s in i["shape"]], i["datatype"])
                    for i in self.metadata["inputs"]
                ]
=======
                    InferInput(i['name'], [int(s) for s in i["shape"]], i['datatype']) for i in self.metadata['inputs']]
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1

        self._create_input_placeholders_fn = create_input_placeholders

    @property
    def runtime(self):
        """Returns the model runtime"""
        return self.metadata.get("backend", self.metadata.get("platform"))

<<<<<<< HEAD
    def __call__(
        self, *args, **kwargs
    ) -> typing.Union[torch.Tensor, typing.Tuple[torch.Tensor, ...]]:
        """Invokes the model. Parameters can be provided via args or kwargs.
=======
    def __call__(self, *args, **kwargs) -> typing.Union[torch.Tensor, typing.Tuple[torch.Tensor, ...]]:
        """ Invokes the model. Parameters can be provided via args or kwargs.
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
        args, if provided, are assumed to match the order of inputs of the model.
        kwargs are matched with the model input names.
        """
        inputs = self._create_inputs(*args, **kwargs)
        response = self.client.infer(model_name=self.model_name, inputs=inputs)
        result = []
<<<<<<< HEAD
        for output in self.metadata["outputs"]:
            tensor = torch.as_tensor(response.as_numpy(output["name"]))
=======
        for output in self.metadata['outputs']:
            tensor = torch.as_tensor(response.as_numpy(output['name']))
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
            result.append(tensor)
        return result[0] if len(result) == 1 else result

    def _create_inputs(self, *args, **kwargs):
        args_len, kwargs_len = len(args), len(kwargs)
        if not args_len and not kwargs_len:
            raise RuntimeError("No inputs provided.")
        if args_len and kwargs_len:
            raise RuntimeError("Cannot specify args and kwargs at the same time")

        placeholders = self._create_input_placeholders_fn()
        if args_len:
            if args_len != len(placeholders):
<<<<<<< HEAD
                raise RuntimeError(
                    f"Expected {len(placeholders)} inputs, got {args_len}."
                )
=======
                raise RuntimeError(f"Expected {len(placeholders)} inputs, got {args_len}.")
>>>>>>> 60ea1aff57f74d50644b9c9aa6008616af5496e1
            for input, value in zip(placeholders, args):
                input.set_data_from_numpy(value.cpu().numpy())
        else:
            for input in placeholders:
                value = kwargs[input.name]
                input.set_data_from_numpy(value.cpu().numpy())
        return placeholders
