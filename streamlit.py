import streamlit as st
import sqlalchemy
import pymysql
import pandas as pd
import altair as alt

page = st.sidebar.radio('Bike sharing Project', ['Active-NonActive stations', 'The Most frequent stations', 'Count of Bikes','Distance between stations','Duration of the loan'])
if page == 'Active-NonActive stations':
    st.title('Active-NonActive stations')
    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
   
    query=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT start_station_name AS Station_name, (countStartStation + countEndStation ) AS CountOfUse
        FROM Bikes 
        WHERE (countStartStation + countEndStation ) < 1000
        
    """
    
    df = pd.read_sql(sql=query,con=engeto_data_conn)
   
   

    chart1=alt.Chart(df).mark_bar().encode(
        x=alt.X('Station_name',sort='y'),
        y='CountOfUse'
    ).interactive()

    st.subheader ('NonActive')
    st.write('Stations with less than 1000 times of use')
    st.altair_chart(chart1, use_container_width=True)



    query1=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT start_station_name AS Station_name, (countStartStation + countEndStation ) AS CountOfUse
        FROM Bikes 
        WHERE (countStartStation + countEndStation ) > 1000
        
    """
    
    df = pd.read_sql(sql=query1,con=engeto_data_conn)
   

    chart2=alt.Chart(df).mark_bar().encode(
        x=alt.X('Station_name',sort='-y'),
        y='CountOfUse'
    ).interactive()
    
    st.subheader('Active')
    st.write('Stations with more than 1000 times of use')
    st.altair_chart(chart2, use_container_width=True)




    
   
elif page == 'The Most frequent stations':
    st.title('Top 10 frequent stations')
    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
    query2=""" 
        WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation DESC
        ) SELECT start_station_name AS Station_name, (countStartStation + countEndStation ) AS CountOfUse FROM Bikes LIMIT 10

    """
    df = pd.read_sql(sql=query2,con=engeto_data_conn)
    st.dateframe(df, use_container_width=True)

    
    chart1=alt.Chart(df).mark_bar().encode(
        x='Station_name',
        y='CountOfUse'
    ).interactive()

    st.altair_chart(chart1, use_container_width=True)

elif page == 'Count of Bikes':
    st.title('Count of Bikes at stations')

    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
   
    query=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT start_station_name AS Station_name, (countEndStation - countStartStation ) AS CountOfUse
        FROM Bikes 
        WHERE (countEndStation - countStartStation ) < 0
    """
    
    df = pd.read_sql(sql=query,con=engeto_data_conn)
   

    chart1=alt.Chart(df).mark_bar().encode(
        x=alt.X('Station_name',sort='y'),
        y='CountOfUse'
    ).interactive()

    st.subheader ('Potentionally missing bikes')
    st.write('Stations where people more start rent of bike than end their rents in the station')
    st.altair_chart(chart1, use_container_width=True)


    query1=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT start_station_name AS Station_name, (countEndStation - countStartStation ) AS CountOfUse
        FROM Bikes 
        WHERE (countEndStation - countStartStation ) > 0
    """
    
    df = pd.read_sql(sql=query1,con=engeto_data_conn)
   

    chart2=alt.Chart(df).mark_bar().encode(
        x=alt.X('Station_name',sort='y'),
        y='CountOfUse'
    ).interactive()

    st.subheader ('Stations with too many bikes')
    st.write('Stations where people more end their rents than start rent of bike in the station')
    st.altair_chart(chart2, use_container_width=True)






elif page == 'Distance between stations':
    st.title('Distance between stations')

    

elif page == 'Duration of the loan':
    st.title('Duration of the loan')