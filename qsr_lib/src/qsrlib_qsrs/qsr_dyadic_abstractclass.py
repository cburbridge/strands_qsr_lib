# -*- coding: utf-8 -*-
from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
from qsrlib_qsrs.qsr_abstractclass import QSR_Abstractclass
from qsrlib_utils.combinations_and_permutations import *
from qsrlib_io.world_qsr_trace import *

class QSR_Dyadic_Abstractclass(QSR_Abstractclass):
    """Abstract class of dyadic QSRs, i.e. QSRs that are computed over two objects.

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor.

        :return:
        """
        super(QSR_Dyadic_Abstractclass, self).__init__()

        # todo should discriminate maybe between points_2d, points_3d, bounding_boxes_2d, bounding_boxes_3d and could possibly go in the QSR_Abstractclass; also maybe refactor to a better name
        self._allowed_dtype = {"points": self.__return_points,
                               "bounding_boxes": self.__return_bounding_boxes}
        """dict: With what data the QSR works with, e.g. with points or with bounding boxes."""

    def _init_qsrs_for_default(self, objects_names_of_world_state):
        """The default list of entities for which QSRs are to be computed for.

        :param objects_names_of_world_state: The objects names at a world state.
        :type objects_names_of_world_state: list
        :return: The permutations, i.e. all possible pairs including mirrors, of the list of names passed in the
        arguments. E.g. for `objects_names_of_world_state = ['a', 'b']` return `[('a', 'b'), ('b', 'a')]`.
        :rtype: list
        """
        return possible_pairs(objects_names_of_world_state)

    def _validate_qsrs_for(self, qsrs_for):
        """Validate `qsrs_for` which must be a list of tuples of two objects names.

        :param qsrs_for: The original `qsrs_for` that needs validation.
        :type qsrs_for: list
        :return: A list of string objects names to make QSRs, which might be the same as the argument `qsrs_for` or a
        subset of it with elements that passed the validation test, i.e. the elements of the list must be tuples of
        two strings.
        :rtype: list
        """
        return [p for p in qsrs_for if isinstance(p, (list, tuple)) and (len(p) == 2)]

    # todo possibly move to QSR_Abstractclass
    def __return_points(self, data1, data2):
        """Return the arguments as they are in their point form.

        :param data1: First object data.
        :type data1: qsrlib_io.world_trace.Object_State
        :param data2: Second object data.
        :type data2: qsrlib_io.world_trace.Object_State
        :return: Return the arguments as they are in their point form.
        :rtype: qsrlib_io.world_trace.Object_State, qsrlib_io.world_trace.Object_State
        """
        return data1, data2

    # todo refactor to __return_bounding_boxes_2d
    # todo possibly move to QSR_Abstractclass
    def __return_bounding_boxes(self, data1, data2):
        """Return the 2D bounding boxes of the arguments.

        :param data1: First object data.
        :type data1: qsrlib_io.world_trace.Object_State
        :param data2: Second object data.
        :type data2: qsrlib_io.world_trace.Object_State
        :return: Return the 2D bounding boxes of the arguments.
        :rtype: list, list
        """

        return data1.return_bounding_box_2d(), data2.return_bounding_box_2d()


class QSR_Dyadic_1t_Abstractclass(QSR_Dyadic_Abstractclass):
    """Special case abstract class of dyadic QSRs.

    Works with dyadic QSRs that require data over one timestamp.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor.

        :return:
        """
        super(QSR_Dyadic_1t_Abstractclass, self).__init__()

    @abstractmethod
    def _compute_qsr(self, data1, data2, qsr_params, **kwargs):
        """Compute QSR value.

        :param data1: First object data.
        :type data1: qsrlib_io.world_trace.Object_State
        :param data2: Second object data.
        :type data2: qsrlib_io.world_trace.Object_State
        :param qsr_params: QSR specific parameters passed in `dynamic_args`.
        :type qsr_params: dict
        :param kwargs: Optional further arguments.
        :return: The computed QSR value.
        :rtype: str
        """
        return

    def make_world_qsr_trace(self, world_trace, timestamps, qsr_params, req_params, **kwargs):
        """Compute the world QSR trace from the arguments.

        :param world_trace: The input data.
        :type world_trace: qsrlib_io.world_trace.World_Trace
        :param timestamps: List of sorted timestamps of `world_trace`.
        :type timestamps: list
        :param qsr_params: QSR specific parameters passed in `dynamic_args`.
        :type qsr_params: dict
        :param dynamic_args: The dynamic arguments passed with the request.
        :type dynamic_args: dict
        :param kwargs: Optional further arguments.
        :return: The computed world QSR trace.
        :rtype: qsrlib_io.world_qsr_trace.World_QSR_Trace
        """
        ret = World_QSR_Trace(qsr_type=self._unique_id)
        for t in timestamps:
            world_state = world_trace.trace[t]
            qsrs_for = self._process_qsrs_for(world_state.objects.keys(), req_params["dynamic_args"])
            for p in qsrs_for:
                between = ",".join(p)
                try:
                    data1, data2 = self._allowed_dtype[self._dtype](world_state.objects[p[0]], world_state.objects[p[1]])
                except KeyError:
                    raise KeyError("%s is not a valid value, should be one of %s" % (self._dtype, self._allowed_dtype.keys()))
                ret.add_qsr(QSR(timestamp=t, between=between,
                                qsr=self._format_qsr(self._compute_qsr(data1, data2, qsr_params, **kwargs))),
                            t)
        return ret