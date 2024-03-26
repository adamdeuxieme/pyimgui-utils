"""Tests that require human validation.

Some feature could not be tested automatically. There is an ImGui test engine
developed by the developers of Dear ImGui project. Unfortunately, this test
engine is only for C++ project and not Python one.

An interactive test consist in opening a window with windows under test and a
contextual window that explains what behavior is expected. You can either mark
a test as passed or failed. Closing the main window will raise an
InteractiveTestException.
"""
