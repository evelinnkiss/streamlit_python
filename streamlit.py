import streamlit as st
import sqlalchemy
import pymysql
import pandas as pd
import altair as alt

page = st.sidebar.radio('Bike sharing Project', ['Active-NonActive stations', 'The Most frequent stations', 'Count of Bikes','Distances between stations','Bike rental time','Bike rent over time'])
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
    st.dataframe(df,1000,300)

    
    chart1=alt.Chart(df).mark_bar().encode(
        x='Station_name',
        y='CountOfUse'
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
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
        ORDER BY CountOfUse DESC
    """
    
    df = pd.read_sql(sql=query1,con=engeto_data_conn)
   

    chart2=alt.Chart(df).mark_bar().encode(
        x=alt.X('Station_name',sort='y'),
        y='CountOfUse'
    ).interactive()

    st.subheader ('Stations with too many bikes')
    st.write('Stations where people more end their rents than start rent of bike in the station')
    st.altair_chart(chart2, use_container_width=True)






elif page == 'Distances between stations':
    st.title('Distances between stations')
    
    from itertools import combinations
    from geopy.distance import geodesic
    import numpy as np

  
    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
    query="""
        SELECT DISTINCT end_station_id  AS id, end_station_name  AS station_name,
        AVG(end_station_latitude) AS lat, 
        AVG(end_station_longitude) AS lng 
        FROM edinburgh_bikes eb
        GROUP BY end_station_id 
        ORDER BY id
    """
    df = pd.read_sql(sql=query,con=engeto_data_conn)
    df = df.set_index('id')

    
    @np.vectorize
    def geodesic_vec(lat1, lon1, lat2, lon2):
        rs = geodesic( (lat1, lon1), (lat2, lon2) ).kilometers
        return rs
    coords = np.array(list(combinations(df[['lat', 'lng']].values, 2)))
    coords = coords.reshape(coords.shape[0], 4)
    distances = geodesic_vec(coords[:, 0], coords[:, 1], coords[:, 2], coords[:, 3])
    combos = list(combinations(df.index, 2))
    dist_df = pd.DataFrame(distances, index=pd.Index(combos, names=['station1', 'station2']), columns=['distance'])
    dist_df = dist_df.join(df.rename_axis('station1')).join(df.rename_axis('station2'), rsuffix='2')
    dist_df
    


elif page == 'Bike rental time':
    st.title('Bike rental time')

    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)

    query="""
        WITH duration AS (
        SELECT start_station_name,end_station_name, ROUND(duration/60,0) AS duration_min, CASE 
            WHEN ROUND(duration/60,0) <=10 THEN '<=10min'
            WHEN ROUND(duration/60,0) >10 AND ROUND(duration/60,0) <=30 THEN '<=30min'
            WHEN ROUND(duration/60,0) >30 AND  ROUND(duration/60,0) <=60 THEN '<=60min_AND_>30min'
            WHEN ROUND(duration/60,0) >60 THEN '>60min'
        END AS duration_type
        FROM edinburgh_bikes eb 
        )SELECT duration_type,COUNT(duration_type) as count
        FROM duration
        GROUP BY duration_type 
    """
    df = pd.read_sql(sql=query,con=engeto_data_conn)


    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('duration_type'),
        y = alt.Y('count')
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
   ).interactive()

    st.altair_chart(hist, use_container_width=True)

elif page == 'Bike rent over time':
    st.title('Development of Bike rent over time')
    
    
    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)

    query="""
        WITH rent_time AS (
            SELECT LEFT(RIGHT(started_at,8),2) AS time , start_station_name  FROM edinburgh_bikes  
        ) SELECT time, COUNT(start_station_name) as countOfRents
        from rent_time  
        group by time 
    """
    df = pd.read_sql(sql=query,con=engeto_data_conn)

    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('time'),
        y = alt.Y('countOfRents')
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
    ).interactive()

    st.altair_chart(hist, use_container_width=True)
