import unittest
from unittest.mock import patch
from rook_attack import build_residual_graph

class TestResidualGraphEdges(unittest.TestCase):

    def check_edges(self, residual_graph, expected_edges):
        actual_edges = set()  

        for u in residual_graph:  
            for v, cap in residual_graph[u].items():  
                if cap > 0:  #We only count edges if capacity > 0
                    actual_edges.add((u, v))  

        # Check for incorrectly added edges
        for edge in actual_edges:
            self.assertIn(edge, expected_edges, f"Incorrectly added edge: {edge}")

        # Ensure all expected edges exist
        for edge in expected_edges:
            self.assertIn(edge, actual_edges, f"Missing expected edge: {edge}")

    @patch('builtins.input', side_effect=["3 3", "X.X", "...", "X.X"])
    def test_case_1_edges(self,mock_input):
        """ Text Case 1 """
        residual_graph, source, sink = build_residual_graph()
        rows, cols = 3, 3

        expected_edges = {
            (source, 0), (source,1),(source,2), # Source connects to all rows
            (0,rows+1), # ROC1 X.X
            (1, rows + 0), (1, rows + 1), (1, rows + 2), #R1C0 R1C1 R1C2 ...
            (2, rows+1), #R2C1 X.X
            (rows + 0, sink), (rows + 1, sink), (rows + 2, sink)  # All cols connect to sink
        }

        self.check_edges(residual_graph, expected_edges)

    @patch('builtins.input', side_effect=["3 3", "...", "...", "..."])
    def test_case_2_no_edges(self,mock_input):
        """ Test Case 2 """
        residual_graph, source, sink = build_residual_graph()
        rows, cols = 3, 3

        expected_edges = {
            (source, 0), (source, 1), (source, 2),  # Source connects to all rows
            (0, rows + 0), (0, rows + 1), (0, rows + 2),  #R0C0 R0C1 R0C2 ...
            (1, rows + 0), (1, rows + 1), (1, rows + 2),  #R1C0 R1C1 R1C2 ...
            (2, rows + 0), (2, rows + 1), (2, rows + 2),  #R2C0 R2C1 R2C2 ...
            (rows + 0, sink), (rows + 1, sink), (rows + 2, sink)  # All cols connect to sink
        }

        self.check_edges(residual_graph, expected_edges)

    @patch('builtins.input', side_effect=["3 3", "X..", "..X", "..X"])
    def test_case_3_edges(self,mock_input):
        """ Test Case 3 """
        residual_graph, source, sink = build_residual_graph()
        rows, cols = 3, 3

        expected_edges = {
            (source,0),(source, 1), (source, 2),  # Source connects to all rows)
            (0,rows+1),(0,rows+2), #R0C1 R0C2 X..
            (1, rows + 0), (1, rows + 1), #R1C0 R1C1 ..X
            (2, rows + 0),  (2, rows + 1), #R2C0 R2C1 ..X
            (rows + 0, sink), (rows+1,sink),(rows + 2, sink)  # All cols connect to sink
        }

        self.check_edges(residual_graph, expected_edges)

if __name__ == "__main__":
    unittest.main()
