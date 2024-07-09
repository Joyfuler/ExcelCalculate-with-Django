from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
from .models import *

def calculate(request):
    file = request.FILES['fileInput']
    print("# 사용자가 등록한 파일 이름 : " , file)
    df = pd.read_excel(file, sheet_name = 'Sheet1', header = 0)
    print(df.head(5))
    
    # 파일 저장
    
    origin_file_name = file.name
    user_name = request.session['user_name']
    now_HMS = datetime.today().strftime('%H%M%S')
    file_upload_name = now_HMS + '_' + user_name + '_' + origin_file_name
    file.name = file_upload_name
    document = Document(user_upload_file = file)
    document.save()
    
    #grade별 value 리스트
    grade_dic = {}
    
    total_row_num = len(df.index)
    for i in range(total_row_num):
        data = df.loc[i]
        if not data['grade'] in grade_dic.keys(): # 만일 존재하지 않는다면 grade_dic에 key 할당.
            grade_dic[data['grade']] = [data['value']]
        else: # 존재한다면 기존과 마찬가지로 기존 data['value']에 접근하여 할당함.
            grade_dic[data['grade']].append(data['value'])
    
    # grade별 최솟값 / 최댓값 평균값 구하기
    grade_calculate_dic = {}
    for key in grade_dic.keys():
        grade_calculate_dic[key] = {}
        grade_calculate_dic[key]['min'] = min(grade_dic[key]) #key의 최소값 대입
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])
    
    
    # 결과출력
    grade_list = list(grade_calculate_dic.keys())
    print("grade list::::" , grade_list)
    grade_list.sort() # 리스트로 출력한 등급별 key값 (최대 / 최소 / 평균) 정렬
    for key in grade_list:
        print("#grade :" , key)
        print("#min :", grade_calculate_dic[key]['min'], end = '')
        print("#max :", grade_calculate_dic[key]['avg'], end = '')
        print("#avg:", grade_calculate_dic[key]['avg'], end = '\n\n')    

    # 이메일 주소 도메인별 인원 구하기
    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i]
        email_domain = (data['email'].split("@"))[1] # 1번인덱스. @ 뒤의 도메인을 분리
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1 # 만일 등록되지 않은 도메인이라면 1로 대입.
        else:
            email_domain_dic[email_domain] += 1
        
    print("도메인별 사용 인원수 : ")           
    for key in email_domain_dic.keys():
        print("#", key, ":" , email_domain_dic[key], '명')
    # return HttpResponse("Calculate, calculte function!")    
    
    grade_calculate_dic_session = {}
    for key in grade_list:
        print("grade list:", key)        
        grade_calculate_dic_session[int(key)] = {}
        grade_calculate_dic_session[int(key)]['max'] = float(grade_calculate_dic[key]['max'])
        grade_calculate_dic_session[int(key)]['min'] = float(grade_calculate_dic[key]['min'])
        grade_calculate_dic_session[int(key)]['avg'] = float(grade_calculate_dic[key]['avg'])
        request.session['grade_calculate_dic'] = grade_calculate_dic_session
        request.session['email_domain_dic'] = email_domain_dic
        return redirect('/result')
    
    

# Create your views here.
