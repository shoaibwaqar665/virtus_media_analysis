from dbOperations import get_signal_from_db, get_urls_from_db



def main():
    signal = get_signal_from_db()
    if signal:
        print("signal", signal)
        result = get_urls_from_db()
        for platform, url in result.items():
            print("platform", platform)
            print("url", url)
            print("--------------------------------")
            
       
    
   

if __name__ == "__main__":
    main()