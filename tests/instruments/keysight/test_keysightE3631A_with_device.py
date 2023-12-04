#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import pytest
from pymeasure.instruments.keysight.keysightE3631A import KeysightE3631A

pytest.skip('Only work with connected hardware', allow_module_level=True)


class TestKeysightE3631A:
    """
    Unit tests for KeysightE3631A class.

    This test suite, needs the following setup to work properly:
        - A KeysightE3631A device should be connected to the computer;
        - The device's address must be set in the RESOURCE constant;
    """

    ##################################################
    # KeysightE3631A device address goes here:
    RESOURCE = "GPIB0::10::INSTR"
    ##################################################

    #########################
    # PARAMETRIZATION CASES #
    #########################

    BOOLEANS = [False, True]
    CHANNELS = [1, 2, 3]

    INSTR = KeysightE3631A(RESOURCE)

    ############
    # FIXTURES #
    ############

    @pytest.fixture
    def instr(self):
        self.INSTR.reset()
        return self.INSTR

    #########
    # TESTS #
    #########

    @pytest.mark.parametrize("case", BOOLEANS)
    def test_output_enabled(self, instr, case):
        assert not instr.output_enabled
        instr.output_enabled = case
        assert instr.output_enabled == case

    @pytest.mark.parametrize("case", BOOLEANS)
    def test_tracking_enabled(self, instr, case):
        assert not instr.tracking_enabled
        instr.tracking_enabled = case
        assert instr.tracking_enabled == case

    @pytest.mark.parametrize("chn, i_limit", [(1, 0), (1, 5), (2, 0), (2, 1), (3, 0), (3, 1)], )
    def test_current_limit(self, instr, chn, i_limit):
        instr.ch(chn).current_limit = i_limit

    @pytest.mark.parametrize("chn, i_limit", [(1, -1), (1, 6), (2, -1), (2, 2), (3, -1), (3, 2)], )
    def test_current_limit_out_of_range(self, instr, chn, i_limit):
        with pytest.raises(ValueError) as not_in_range:
            instr.ch(chn).current_limit = i_limit
            assert f"Value of {i_limit} is not in range" in not_in_range

    @pytest.mark.parametrize("chn, voltage", [(1, 0), (1, 6), (2, 0), (2, 25), (3, 0), (3, -25)], )
    def test_voltage_setpoint(self, instr, chn, voltage):
        instr.ch(chn).voltage_setpoint = voltage
        assert instr.ch(chn).voltage_setpoint == voltage

    @pytest.mark.parametrize("chn, voltage", [(1, -1), (1, 7), (2, -1), (2, 26), (3, 1), (3, -26)], )
    def test_voltage_setpoint_out_of_range(self, instr, chn, voltage):
        with pytest.raises(ValueError) as not_in_range:
            instr.ch(chn).voltage_setpoint = voltage
            assert f"Value of {voltage} is not in range" in not_in_range

    @pytest.mark.parametrize("chn", CHANNELS)
    def test_measure_voltage(self, instr, chn):
        assert type(instr.ch(chn).voltage) == float

    @pytest.mark.parametrize("chn", CHANNELS)
    def test_measure_current(self, instr, chn):
        assert type(instr.ch(chn).current) == float
