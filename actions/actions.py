import string
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from  rasa_sdk.executor import  CollectingDispatcher
import mysql.connector
import feedparser
import re

from datetime import datetime

class action_category(Action):

    def name(self) -> Text:
        return "action_category"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            categoryVariable = tracker.get_slot("category")
            # if(categoryVariable=="Lập trình wed" or "lap trinh wed"):
            #     categoryVariable= "Lập trình web"
            categoryArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCategory = "SELECT * FROM categories WHERE title LIKE '%{}%'".format(categoryVariable)
            curCourse.execute(codeOfCategory)
            result = curCourse.fetchall()
            for x in result:
                categoryArray.append(x[0])

            db.rollback()
            db.close()

            if (len(categoryArray) > 0): 
                codeOfVariable = categoryArray[0]
                courseReturn = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                curCourse = db.cursor()
                codeOfCategory = "SELECT * FROM course WHERE category_id LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCategory)
                result = curCourse.fetchall()
                if(len(result)):
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                    dispatcher.utter_message("Các khóa học " + categoryVariable + " hiện có tại website là: ")
                    for  x in (courseReturn):
                        i=1
                        dispatcher.utter_message( x)
                        i=i+1
                    
                    return []
                else:
                    dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")


class action_allCategory(Action):

    def name(self) -> Text:
        return "action_allCategory"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            categoryVariable = tracker.get_slot("allcategory")
            categoryArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCategory = "SELECT * FROM categories"
            curCourse.execute(codeOfCategory)
            result = curCourse.fetchall()
            for x in result:
                categoryArray.append(x[1])

            db.rollback()
            db.close()

            if (len(categoryArray) > 0): 
                dispatcher.utter_message("Tất cả các danh mục hiện có tại website là: ")
                for  x in (categoryArray):
                    dispatcher.utter_message( x)
                
                return []
                
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_courseCode(Action):

    def name(self) -> Text:
        return "action_courseCode"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("course_code")
            courseArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[1])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                courseReturn = courseArray[0]
                dispatcher.utter_message("Khóa học có mã khóa học " + courseVariable + " là: ")
                dispatcher.utter_message(courseReturn)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_instructor(Action):

    def name(self) -> Text:
        return "action_instructor"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("instructor")
            courseVariable2 = string.capwords(courseVariable)
            course_codeArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course_detail WHERE instructor LIKE '{}'".format(courseVariable2)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                course_codeArray.append(x[1])

            db.rollback()
            db.close()


            if (len(course_codeArray) > 0):
                courseReturn = []
                for x in course_codeArray:
                    codeOfVariable = x

                    db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                    curCourse = db.cursor()
                    codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                    curCourse.execute(codeOfCourse)
                    result = curCourse.fetchall()
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                dispatcher.utter_message("Các khóa học do thầy " + courseVariable2 + " giảng dạy là: ")
                for  x in courseReturn:
                    dispatcher.utter_message(x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_duration(Action):

    def name(self) -> Text:
        return "action_duration"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("duration")

            course_codeArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course_detail WHERE duration LIKE '{}'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                course_codeArray.append(x[1])

            db.rollback()
            db.close()


            if (len(course_codeArray) > 0):
                courseReturn = []
                for x in course_codeArray:
                    codeOfVariable = x

                    db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                    curCourse = db.cursor()
                    codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                    curCourse.execute(codeOfCourse)
                    result = curCourse.fetchall()
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                dispatcher.utter_message("Các khóa học có thời gian học " + courseVariable + " tuần là: ")
                for  x in courseReturn:
                    dispatcher.utter_message(x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")



class action_skillLevel(Action):

    def name(self) -> Text:
        return "action_skillLevel"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("skill_level")
            skill_level = 0
            if (courseVariable=="cơ bản"):
                skill_level = 0
            elif (courseVariable=="nâng cao"):
                skill_level = 1
            course_codeArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course_detail WHERE skill_level LIKE '{}'".format(skill_level)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                course_codeArray.append(x[1])

            db.rollback()
            db.close()


            if (len(course_codeArray) > 0):
                courseReturn = []
                for x in course_codeArray:
                    codeOfVariable = x

                    db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                    curCourse = db.cursor()
                    codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                    curCourse.execute(codeOfCourse)
                    result = curCourse.fetchall()
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                dispatcher.utter_message("Các khóa học có trình độ " + courseVariable + " là: ")
                for  x in courseReturn:
                    dispatcher.utter_message(x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_language(Action):

    def name(self) -> Text:
        return "action_language"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("language")

            course_codeArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course_detail WHERE language LIKE '{}'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                course_codeArray.append(x[1])

            db.rollback()
            db.close()
            if (len(course_codeArray) > 0):
                courseReturn = []
                for x in course_codeArray:
                    codeOfVariable = x

                    db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                    curCourse = db.cursor()
                    codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                    curCourse.execute(codeOfCourse)
                    result = curCourse.fetchall()
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                dispatcher.utter_message("Các khóa học ngôn ngữ " + courseVariable + " là: ")
                for x in (courseReturn):
                    dispatcher.utter_message(x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")


class action_startDay(Action):

    def name(self) -> Text:
        return "action_startDay"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("start_day")
            year=0
            month = 0
            courseList = list(courseVariable)
            for i in courseList:
                if i == "/":
                    courseVariable = courseVariable.replace("/", "-")
            oldString = courseVariable.split("-")
            # if (oldString[0] == "2022"):
            #     newString = oldString[0] + "-" + oldString[1] + "-" + oldString[2]
            # else:
            #     newString = oldString[2] + "-" + oldString[1] + "-" + oldString[0]
            if (oldString[0] == "2022"):
                year = oldString[0]
                month = oldString[1]
            else:
                year = oldString[1]
                month = oldString[0]
            course_codeArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course_detail WHERE MONTH(start_day) LIKE '{}' AND YEAR (start_day) LIKE '{}'".format(month,year)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                course_codeArray.append(x[1])

            db.rollback()
            db.close()


            if (len(course_codeArray) > 0):
                courseReturn = []
                for x in course_codeArray:
                    codeOfVariable = x

                    db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                    curCourse = db.cursor()
                    codeOfCourse = "SELECT * FROM course WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                    curCourse.execute(codeOfCourse)
                    result = curCourse.fetchall()
                    for x in result:
                        courseReturn.append(x[1])
                    db.rollback()
                    db.close()
                dispatcher.utter_message("Các khóa học bắt đầu vào ngày " + courseVariable + " là: ")
                for i,x in (courseReturn):
                    dispatcher.utter_message(x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_courseName(Action):

    def name(self) -> Text:
        return "action_courseName"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("course_name")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[4])
                courseName.append(x[1])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):

                for i,x in enumerate(courseArray):
                    dispatcher.utter_message("Khóa học "+courseName[i]+ " có mã khóa học là: " +x)

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_detailCourse(Action):

    def name(self) -> Text:
        return "action_detailCourse"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("detail")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[2])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                dispatcher.utter_message("Chi tiết khóa học " + courseVariable + " là: ")
                for x in courseArray:
                    dispatcher.utter_message("Để biết thêm thông tin chi tiết vui lòng đọc thêm tại đây: http://localhost/tiny_educate/public/chi-tiet/" +str(courseArray[0]))

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_nameStartDay(Action):

    def name(self) -> Text:
        return "action_nameStartDay"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("nameStartDay")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[4])
                courseName.append(x[1])
            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                codeOfVariable = courseArray[0]
                courseReturn = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                curCourse = db.cursor()
                codeOfCourse = "SELECT * FROM course_detail WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCourse)
                result = curCourse.fetchall()
                for x in result:
                    courseReturn.append(x[5])
                db.rollback()
                db.close()
                for x in (courseReturn):
                    dispatcher.utter_message("Khóa học "+courseVariable+ " có thời gian bắt đầu là: " +datetime.strftime(x,"%Y/%m/%d"))

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_nameCost(Action):

    def name(self) -> Text:
        return "action_nameCost"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("nameCost")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[4])
                courseName.append(x[1])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                codeOfVariable = courseArray[0]
                courseReturn = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                curCourse = db.cursor()
                codeOfCourse = "SELECT * FROM course_detail WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCourse)
                result = curCourse.fetchall()
                for x in result:
                    courseReturn.append(x[8])
                db.rollback()
                db.close()
                for x in courseReturn:
                    dispatcher.utter_message("Khóa học "+courseVariable+ " có giá tiền là: " +str(x) + "VNĐ")

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_nameDuration(Action):

    def name(self) -> Text:
        return "action_nameDuration"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("nameDuration")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[4])
                courseName.append(x[1])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                codeOfVariable = courseArray[0]
                courseReturn = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                curCourse = db.cursor()
                codeOfCourse = "SELECT * FROM course_detail WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCourse)
                result = curCourse.fetchall()
                for x in result:
                    courseReturn.append(x[4])
                db.rollback()
                db.close()
                for x in (courseReturn):
                    dispatcher.utter_message("Khóa học "+courseVariable+ " có thời gian học : " +x +" tuần")

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_teacherCourse(Action):

    def name(self) -> Text:
        return "action_teacherCourse"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("teachercourse")
            courseArray = []
            courseName = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM course WHERE title LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[4])
                courseName.append(x[1])

            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                codeOfVariable = courseArray[0]
                courseReturn = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="tiny_educate")
                curCourse = db.cursor()
                codeOfCourse = "SELECT * FROM course_detail WHERE course_code LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCourse)
                result = curCourse.fetchall()
                for x in result:
                    courseReturn.append(x[2])
                db.rollback()
                db.close()
                for x in (courseReturn):
                    dispatcher.utter_message("Người dạy khóa học "+courseVariable+ " là : " +x )

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_Contact(Action):

    def name(self) -> Text:
        return "action_Contact"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            categoryVariable = tracker.get_slot("contact")
            categoryArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd ="", database="tiny_educate")
            curCourse = db.cursor()
            codeOfCategory = "SELECT * FROM contacts"
            curCourse.execute(codeOfCategory)
            result = curCourse.fetchall()
            for x in result:
                categoryArray.append(x[2] + " " + x[3])

            db.rollback()
            db.close()

            dispatcher.utter_message("Địa chỉ liên hệ trung tâm là: ")
            for  x in (categoryArray):
                dispatcher.utter_message( x)
            
            return []
                

        except:
            dispatcher.utter_message("Tôi không hiểu!")
