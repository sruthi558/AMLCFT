@app.route('/MLRONextLevel', methods=['GET', 'POST'])
def MLRONextLevel(): 
    success_message = session.pop('success_message', None)
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    mlro_email = session['email_id']
    # print("mlro_email",mlro_email)
    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
        return "User data not found. Please log in again."

    ticket_numbers = mlro.get("mlros", [])
    
    data = {}
    headers = set()
    codes = set()
    collections = [TY_collection,TM_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
      
    
    for ticket_number in ticket_numbers:
        for collection in collections:
            for array_name in array_names:
                data_from_collection = collection.find_one(
                    {
                        "$and": [
                            
                            {f"{array_name}.allocate_to": mlro_email},
                            {f"{array_name}.ticket_id": ticket_number},
                           

                        ]
                    }
                )
                # print("data_from_collection",data_from_collection)
                

                if data_from_collection:
                        code = data_from_collection.get("code")

                        # Initialize an empty list if the code is not in data
                        if code not in data:
                            data[code] = []

                        # Extract specific objects from the array that meet the criteria
                        matched_objects = [
                            obj for obj in data_from_collection[array_name] if obj["ticket_id"] == ticket_number and obj["levels"]["mlro_level"] is None
                        ]
                        # Add the matched objects to the list for the code
                        data[code].extend(matched_objects)

                        headers.update(data_from_collection.keys())
                    

    return render_template('alertOperationMLRO.html', data=data,success_message=success_message)