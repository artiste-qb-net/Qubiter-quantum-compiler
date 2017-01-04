from CktEmbedder import *  # if don't include this, can't find Controls
from EchoingSEO_reader import *
from quantum_compiler.DiagUnitarySEO_writer import *


class DiagUnitaryExpander(EchoingSEO_reader):
    """
    This class is a child of EchoingSEO_reader. The class reads any
    previously created Qubiter English file and it writes new English &
    Picture files wherein every line of the original English file that
    doesn't start with DIAG (diagonal unitary, aka d-unitary) is echoed
    faithfully whereas lines which do start with DIAG are expanded via class
    DiagUnitarySEO_writer into a sequence in the style specified as input to
    the class constructor.

    So, to expand English & Picture files that contain DIAG and MP_Y lines
    into just CNOTs and qubit rotations, first use this class and the
    analogous one for MP_Y, then use class CktExpander.

    If the input English file has in_file_prefix as file prefix, then the
    output English & Picture files have as file prefix in_file_prefix + '_X1',
    assuming that '_X' + str(k) for some integer k is not already the ending
    of in_file_prefix. If it is, then the ending is changed to '_X' + str(
    k+1).


    Attributes
    ----------
    num_ops : int
        number of operations. Lines inside a loop with 'reps' repetitions
        will count as 'reps' operations
    loop_to_cur_rep : dict[int, int]
        a dictionary mapping loop number TO current repetition
    just_jumped : bool
        flag used to alert when loop jumps from NEXT to LOOP
    line_count : int

    english_in : _io.TextIOWrapper
        file object for input text file that stores English description of
        circuit
    file_prefix : str
        beginning of the name of English file being scanned
    loop_to_start_line : dict[int, int]
        a dictionary mapping loop number TO loop line + 1
    loop_to_start_offset : dict[int, int]
        a dictionary mapping loop number TO offset of loop's start
    loop_to_reps : dict[int, int]
        a dictionary mapping loop number TO total number of repetitions of
        loop
    loop_queue : list[int]
        a queue of loops labelled by their id number
    num_bits : int
        number of qubits in whole circuit
    tot_num_lines : int
        number of lines in English file
    split_line : list[str]
        storage space for a list of strings obtained by splitting a line

    verbose : bool

    gbit_list : list(int)
        Only needed if expanding DIAG's in oracular style, this is a list of
        grounded bits
    wr : DiagUnitarySEO_writer
        This object of DiagUnitarySEO_writer, created in the class
        constructor, is called inside every use_  function to do some writing
        in the output files.

    """

    def __init__(self, file_prefix, num_bits, style, gbit_list=None):
        """
        Constructor

        Parameters
        ----------
        file_prefix : str
        num_bits : int
        style : str
        gbit_list : list(int)

        Returns
        -------
        None

        """

        if gbit_list:
            num_gbits = len(gbit_list)
        else:
            num_gbits = 0

        # default embedder and rad_angles
        emb = CktEmbedder(num_bits, num_bits)
        rad_angles = None
        out_file_prefix = SEO_reader.xed_file_prefix(file_prefix)
        wr = DiagUnitarySEO_writer(out_file_prefix, emb,
            style, rad_angles, num_gbits=num_gbits)

        EchoingSEO_reader.__init__(self, file_prefix, num_bits, wr, style,
                                   gbit_list)

        self.wr.close_files()

    def emb_for_du(self, controls):
        """
        This is an internal function used inside the function use_DIAG().
        This function returns emb, nt, nf to be used as arguments of a
        DiagUnitarySEO_writer that will be used to expand the DIAG line
        currently being considered. emb is a circuit embedder, nt is the
        number of T bits and nf is the number of F bits detected in the
        input argument 'controls'.

        Parameters
        ----------
        controls : Controls
            controls of the DIAG currently being considered.

        Returns
        -------
        CktEmbedder, int, int

        """
        T_bpos = []
        F_bpos = []
        MP_bpos = []
        for bpos, kind in controls.bit_pos_to_kind.items():
            # int is subclass of bool
            # so isinstance(x, int) will be true for x bool too!
            if isinstance(kind, bool):
                if kind:
                    T_bpos.append(bpos)
                else:
                    F_bpos.append(bpos)
            else:
                MP_bpos.append(bpos)
        T_bpos.sort()
        F_bpos.sort()
        MP_bpos.sort()
        if self.gbit_list:
            g_bpos = self.gbit_list.sort()
        else:
            g_bpos = []
        bit_map = T_bpos + F_bpos + MP_bpos + g_bpos
        # print("bit_map", bit_map)
        assert len(bit_map) == len(set(bit_map)),\
            "bits used to define d-unitary are not unique"
        assert len(bit_map) <= self.num_bits

        nt = len(T_bpos)
        nf = len(F_bpos)
        emb = CktEmbedder(num_bits, num_bits, bit_map)
        return emb, nt, nf

    def use_DIAG(self, controls, rad_angles):
        """
        This is an override of a function in the parent class
        EchoingSEO_reader. This is the only use_ function of this class that
        doesn't simply echo its input line. This function does most of its
        work inside the DiagUnitary_SEO_writer.write() function that it calls.

        Parameters
        ----------
        controls : Controls
        rad_angles : list[float]

        Returns
        -------
        None

        """

        emb, nt, nf = self.emb_for_du(controls)
        self.wr.emb = emb
        self.wr.rad_angles = rad_angles
        self.wr.num_T_trols = nt
        self.wr.num_F_trols = nf
        # style and num_gbits for wr are set by constructor

        self.wr.write()
        # revert to default embedder
        self.wr.emb = CktEmbedder(self.num_bits, self.num_bits)

if __name__ == "__main__":
    num_bits = 6
    file_prefix = "../io_folder/d_unitary_test_one_line"
    style = 'exact'
    xer = DiagUnitaryExpander(file_prefix, num_bits, style)

