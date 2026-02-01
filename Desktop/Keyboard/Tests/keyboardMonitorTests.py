from types import SimpleNamespace
from Desktop.Keyboard.keyboardMonitor import KeyboardMonitor

class KeyboardMonitorTests:
    def __init__(self):
        """ Create a monitor to check the keyboard

        Attributes:
        - Monitor (KeyboardMonitor): Monitor for keyboard

        Returns:
        - None
        """
        self.Monitor = KeyboardMonitor()

    def Simulate(self, EventType):
        """ Given a keyboard event, simulate if the monitor detect a key is pressed

        Arguments:
        - EventType (string): An interaction with the keyboard

        Returns:
        - (bool): True if pressed else false
        """
        if EventType is not None:
            Event = SimpleNamespace(event_type=EventType)
            self.Monitor.OnKey(Event)
        return self.Monitor.Live()
    
    def TestNothingPressed(self):
        """ Test no key is pressed

        Returns:
        - (bool): True if no key is pressed
        """
        return self.Simulate(None) is False 
    
    def TestKeyPressed(self):
        """ Test if key is pressed

        Returns:
        - (bool): True if key is pressed
        """
        return self.Simulate("down") is True 

    def RunAllTests(self):
        """ Run all tests for keyboard monitoring

        Returns:
        - None
        """
        Results = {
            "Nothing Pressed": self.TestNothingPressed(),
            "Key Pressed": self.TestKeyPressed()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = KeyboardMonitorTests()
    Tests.RunAllTests()
