#!/bin/python
import active
import unittest
import numpy as np;
from Matrix_Utils import *;

class ActiveTester(unittest.TestCase):
    def test_active(self):
        a        = np.array([[1,2],[0,0]]);
        
        standard   = np.array([[0.7310585786300049,0.8807970779778823],[0.5,0.5]]);
        a_sgmoid   = active.active(a);
        #matrix_show(a_sgmoid);
        #matrix_show(standard);
        self.assertEqual(is_matrix_equals(a_sgmoid, standard), True);
                
        a_linear = active.active(a, 'linear');
        self.assertEqual(is_matrix_equals(a_linear,a), True); 

        with self.assertRaises(Exception):
            active.active(a,"unknown active_type")

    def test_loss(self):
        a   = np.array([[0.1,0.2],[0.3,0.9]]);
        y   = np.array([[1,0],[0,1]]);
        idx = np.array([[1,1],[1,0]]);

        loss = active.loss(a,y);
        self.assertLess(abs(loss-2.987764103904814), 0.000001);
        loss = active.loss(a,y,idx=idx);
        self.assertLess(abs(loss-2.8824035882469876), 0.000001);

        loss = active.loss(a,y,"least_square");
        self.assertLess(abs(loss-0.9500000000), 0.000001);        
        loss = active.loss(a,y,"least_square",idx);
        self.assertLess(abs(loss-0.9400000000), 0.000001);
        

        a = np.array([[0.1,0.2], [3,9]]);
        y = np.array([[1,0],[0,1]]);
        idx = np.array([[0,1],[1,1]]);
        loss = active.loss(a,y,"appro_l1_hinge");
        self.assertLess(abs(loss - 6.091), 0.0000001);
        loss = active.loss(a,y,"appro_l1_hinge", idx);
        self.assertLess(abs(loss-(6.091-0.891)), 0.00000001);

        loss = active.loss(a,y,"l2_hinge");
        self.assertLess(abs(loss - 18.25), 0.0000001);
        loss = active.loss(a,y,"l2_hinge",idx);
        self.assertLess(abs(loss - (18.25-0.81)), 0.0000001);

        with self.assertRaises(Exception):
            active.loss(a,y, "unkonw loss");
        

    def test_grad(self):
        a = np.array([[0.1, 0.2], [0.3, 0.9]]);
        y = np.array([[1,   0],   [0,   1]]);

        with self.assertRaises(Exception):
            active.grad(a, type = "sgmoid_negativeloglikelihood");
            active.grad(a, type = "linear_least_square");
            active.grad(a, type = "linear_approx_l1_hinge");
            active.grad(a, type = "linear_l2_hinge");
        
        grad = active.grad(a, y, type = "sgmoid_negativeloglikelihood");
        tx   = np.array([[-0.9,0.2],[0.3,-0.1]]);
        self.assertTrue(is_matrix_equals(grad, tx), True);
 
        grad = active.grad(a, type = "sgmoid");
        tx   = np.array([[0.09,0.16],[0.21,0.09]]);
        self.assertTrue(is_matrix_equals(grad, tx), True);

        grad = active.grad(a, type = "linear");
        tx   = np.array([[1,1],[1,1]]);
        self.assertTrue(is_matrix_equals(grad, tx), True);

        grad = active.grad(a, type = "tanh");
        tx   = np.array([[0.99,0.96],[0.91,0.19]]);
        self.assertTrue(is_matrix_equals(grad,tx), True);

        with self.assertRaises(Exception):
            active.grad(a,y, "unknow active_type");