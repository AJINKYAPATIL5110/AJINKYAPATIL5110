current_date = date.today()
            input_date = datetime.strptime(date1, "%Y-%m-%d")
            current_time = datetime.now()
            input_time=int(current_time.strftime("%H-%m"))

            if input_date.date() < current_date:
                msg="Not Available"
                return render_template("book.html",msg2=msg)
            
            if not found2:
                for i in range(1,9):
                    add_slot=slot_available(name=slot1[slot[i-1]],date1=date1,availability=0,duration=slot[i-1])
                    db.session.add(add_slot)
                    db.session.commit()

            found3=slot_available.query.filter((slot_available.name)>=input_time,slot_available.date1==date1,slot_available.availability==0).all()

            if found3:
                temp_data2=temp_data.query.filter_by(d_id=department_id).first()
                if temp_data2:
                    db.session.delete(temp_data2)
                    db.session.commit()

                temp_data1=temp_data(p_name=p_name,year=year,branch=branch,d_id=department_id,date1=date1)
                db.session.add(temp_data1)
                db.session.commit()
                msg=1
                return render_template('book.html',msg1=msg,slots=found3)
            else:
                msg="Slots are full"