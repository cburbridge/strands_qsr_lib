# -*- coding: utf-8 -*-
from __future__ import print_function, division
from qsrlib_qsrs.qsr_triadic_abstractclass import QSR_Triadic_1t_Abstractclass
import math

class QSR_TPCC(QSR_Triadic_1t_Abstractclass):
    """ TPCC QSRs.
    .. seealso:: For further details about TPCC, see http://www.sfbtr8.spatial-cognition.de/project/r3/QualitativeCalculi/TPCC/index.html.
    """
    _unique_id = "tpcc"
    _all_possible_relations = ('dlf', 'dfl', 'dsl', 'dbl', 'dlb', 'dsb', 'drb', 'dbr',
                               'dsr', 'dfr', 'drf', 'dsf', 'clf', 'cfl', 'csl', 'cbl',
                               'clb', 'csb', 'crb', 'cbr', 'csr', 'cfr', 'crf', 'csf',
                               'sam')
    _dtype = "points"
    __partition_names = ['bl','lb','lf','fl','fr','rf','rb','br']

    def __init__(self):
        """Constructor."""
        super(QSR_TPCC, self).__init__()

    def _compute_qsr(self, origin, relatum, objct, qsr_params, **kwargs):
        base_distance = math.sqrt((origin.x-relatum.x)**2 + (origin.y-relatum.y)**2)
        object_distance  = math.sqrt((objct.x-relatum.x)**2 + (objct.y-relatum.y)**2)
        if base_distance == object_distance:
            return "sam"
        
        relation = "d" if object_distance > base_distance else "c" # is it far or close: first letter
        
        angle = self._relative_angle(origin, relatum, objct)
        partition = int(angle / 8) #TODO: the "*s*" relations
        relation += self.__partition_names[partition]
        
        return relation

    @staticmethod
    def _relative_angle(a, b, c):
        """Compute relative angle used to select the (left/right/straight/front/back/straight)
        relationship"""
        angle_BA = math.atan2((b.y - a.y),(b.x - a.x))
        
        if angle_BA < 0:
            angle_BA += 2 * math.pi
            
        angle_CB = math.atan2((c.y - b.y), (c.x - b.x))
        if angle_CB < 0:
            angle_CB += 2 * math.pi
            
        angle_rel = angle_CB - angle_BA
        if angle_rel < 0:
            angle_rel += 2 * math.pi
        
        return angle_rel