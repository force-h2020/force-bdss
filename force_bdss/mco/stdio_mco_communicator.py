import sys

from force_bdss.api import BaseMCOCommunicator, DataValue


class StdIOMCOCommunicator(BaseMCOCommunicator):
    """ The StdIOMCOCommunicator is responsible for handing the communication
    protocol between the MCO executable (for example, the dakota executable) and
    the single point evaluation (our BDSS in --evaluate mode).

    The StdIOMCOCommunicator implements the communication using stdin and stdout.
    """

    def receive_from_mco(self, model):
        """Receives data from the MCO (e.g. dakota) by reading from
        standard input the sequence of numbers that are this execution's
        parameter values.

        You can use fancier communication systems here if your MCO supports
        them.
        """
        data = sys.stdin.read()
        values = list(map(float, data.split()))
        names = [p.name for p in model.parameters]
        types = [p.type for p in model.parameters]

        # The values must be given a type. The MCO may pass raw numbers
        # with no type information. You are free to use metadata your MCO may
        # provide, but it is not mandatory that this data is available. You
        # can also use the model specification itself.
        # In any case, you must return a list of DataValue objects.
        return [
            DataValue(type=_type, name=name, value=value)
            for _type, name, value in zip(types, names, values)
        ]

    def send_to_mco(self, model, data_values):
        """ Sends the data_values.values to stdout via string format. Once the
        single point evaluation is completed, this method is used to send the
        data back to the MCO via stdout.

        Parameters
        ----------
        model: any
        data_values: List[DataValue]
            List of DataValues to send to stdout

        Stdout
        ----------
        data: str
            A string of DataValue.values separated by " "..
        """
        data = " ".join([str(dv.value) for dv in data_values])
        sys.stdout.write(data)
