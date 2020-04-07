"""
English DistilGPT-2 model abstraction.
"""

import transformers


MODEL_NAME = 'distilgpt2'
MINUMUM_LENGTH = 20


class DistilGPT2:
    """
    Hugging Face's transformers DistilGPT-2 model abstraction.
    """

    def __init__(self):
        """
        Initializer.

        :returns: nothing
        """

        # setup model for inference
        self.__setup()


    def __setup(self):
        """
        Setup model for inference tasks.

        :returns: nothing
        """

        # load model tokenizer
        self.__tokenizer = transformers.AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        # load model weights
        self.__model = transformers.AutoModelWithLMHead.from_pretrained(
            MODEL_NAME
        )


    def predict(self, sequence, max_length = 150):
        """
        Predicts the next words from a sequence within a maximum length.

        :param sequence: initial sequence
        :type  sequence: str

        :param max_length: prediction maximum length
        :type  max_length: int

        :returns: predicted sequence
        :rtype: str
        """

        # tokenize input sequence as pytorch tensor
        tokenized = self.__tokenizer.encode(sequence, return_tensors = 'pt')

        # predict next tokens
        predicted = self.__model.generate(tokenized,
                                          min_length = MINUMUM_LENGTH,
                                          max_length = max_length,
                                          do_sample = True,
                                          repetition_penalty = float('inf'))

        # return decoded generated sequence
        return self.__tokenizer.decode(predicted.tolist()[0])
