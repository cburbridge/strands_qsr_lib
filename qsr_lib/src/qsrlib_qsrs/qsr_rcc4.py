# -*- coding: utf-8 -*-
from __future__ import print_function, division
from qsrlib_qsrs.qsr_rcc_abstractclass import QSR_RCC_Abstractclass


class QSR_RCC4(QSR_RCC_Abstractclass):
    """Computes symmetrical RCC4 relations"""

    _unique_id = "rcc4"

    _all_possible_relations = ("dc", "po", "pp", "ppi")

    __mapping_from_rcc8 = {"dc": "dc",
                           "ec": "po",
                           "po": "po",
                           "tpp": "pp",
                           "ntpp": "pp",
                           "eq": "pp",
                           "tppi": "ppi",
                           "ntppi": "ppi"}

    def __init__(self):
        super(QSR_RCC4, self).__init__()

    def _convert_to_requested_rcc_type(self, qsr):
        return self.__mapping_from_rcc8[qsr]
