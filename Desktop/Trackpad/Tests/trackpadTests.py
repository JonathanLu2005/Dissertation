from Desktop.Trackpad.trackpad import TrackpadMonitor 

class TrackpadMonitorTests:
    def __init__(self):
        """ Establish monitor to test

        Attributes:
        - Monitor (TrackpadMonitor): Trackpad monitor

        Returns:
        - None
        """
        self.Monitor = TrackpadMonitor()

    def TestMove(self):
        """ Test tracking movement

        Returns:
        - (bool): True if mouse moved else false
        """
        self.Monitor.TrackMove(100, 200)
        return self.Monitor.LiveMove()
    
    def TestClick(self):
        """ Test tracking clicking

        Returns:
        - (bool): True if mouse clicked else false
        """
        self.Monitor.TrackClick(100, 200, None, True)
        return self.Monitor.LiveClick()
    
    def TestScroll(self):
        """ Test tracking scrolling

        Returns:
        - (bool): True if mouse scrolled else false
        """
        self.Monitor.TrackScroll(100, 200, 0, -1)
        return self.Monitor.LiveScroll()
    
    def TestNothing(self):
        """ Test if nothing happens

        Returns:
        - (bool): True if nothing happens else false
        """
        Movement = self.Monitor.LiveMove()
        Clicked = self.Monitor.LiveClick()
        Scrolled = self.Monitor.LiveScroll()
        return not (Movement and Clicked and Scrolled)
    
    def RunAllTests(self):
        """ Run all tests for trackpad monitoring
        
        Returns:
        - None
        """
        Results = {
            "Movement": self.TestMove(),
            "Clicked": self.TestClick(),
            "Scroll": self.TestScroll(),
            "Nothing": self.TestNothing()
        }

        Passed = sum(1 for r in Results.values() if r)
        Total = len(Results)

        print("\nTest Summary:")
        for Name, Result in Results.items():
            print(f" - {Name}: {'PASS' if Result else 'FAIL'}")

        print(f"\nFinal Result: {Passed}/{Total} tests passed.")

if __name__ == "__main__":
    Tests = TrackpadMonitorTests()
    Tests.RunAllTests()