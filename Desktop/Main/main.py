from Desktop.Background import background
import time

def main():
    """ Calls computer vision components
    
    Returns:
    - None
    """
    print("Starting Laptop Background Monitor...")
    Monitor = background.BackgroundMonitor()

    try:
        while True:
            Changed, Ratio = Monitor.Run()
            time.sleep(0.5) 
    except KeyboardInterrupt:
        print("Stopping monitoring...")
    finally:
        Monitor.Release()

if __name__ == "__main__":
    main()