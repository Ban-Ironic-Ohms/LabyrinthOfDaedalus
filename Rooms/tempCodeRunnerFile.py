    if input_command == "inspect":
        desc = dataset["description"]
        print(f"you see {desc}")
        
        get_poi(dataset)
       
        return input_handler(dataset=dataset)