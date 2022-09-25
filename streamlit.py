from email.quoprimime import body_length
import streamlit as st
import sqlalchemy
import pymysql
import pandas as pd
import altair as alt



st.set_page_config(layout="wide")
page = st.sidebar.radio('Bike sharing Project', ['1. Active-NonActive stations', '2. The Most frequent stations', '3. Count of Bikes','4. Distances between stations','5. Bike rental time','Demand analysis'])
if page == '1. Active-NonActive stations':
    
    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)
    query=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT 
                DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT 
        (countStartStation + countEndStation ) AS CountOfUse
        FROM Bikes 
        
    """

    
    df = pd.read_sql(sql=query,con=engeto_data_conn)
    df = pd.DataFrame(df) 
    df = df.describe().round(0)
   


    st.title('Active-NonActive stations')
    st.write('identifikujte aktivní a neaktivní stanice')
    st.write("25% percentil",df['CountOfUse'].iloc[4],"použití.")
   
    query0=""" 
       WITH bikes AS (
            SELECT DISTINCT start_station_name, 
            COUNT(start_station_id)  AS countStartStation,
            countEndStation 
            FROM edinburgh_bikes a
            INNER JOIN (
                SELECT 
                DISTINCT end_station_name, 
                COUNT(end_station_id)  AS countEndStation 
                FROM edinburgh_bikes eb 
                GROUP BY end_station_name 
            ) b
            ON a.start_station_name=b.end_station_name
            GROUP BY start_station_name 
            ORDER BY countStartStation 
        ) SELECT 
        start_station_name AS Station_name, 
        (countStartStation + countEndStation ) AS CountOfUse
        FROM Bikes 
        WHERE (countStartStation + countEndStation ) <= 434
        
    """

    df = pd.read_sql(sql=query0,con=engeto_data_conn)

    chart1 = alt.Chart(df).mark_bar().encode(
        x = alt.X('Station_name',sort='y'),
        y = 'CountOfUse',
        tooltip = [ 'Station_name','CountOfUse' ]
    ).interactive()

    st.subheader ('NonActive')
    st.write('Stations with less than 434 times of use')
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
        WHERE (countStartStation + countEndStation ) > 434
        
    """
    
    df = pd.read_sql(sql=query1,con=engeto_data_conn)
   

    chart2 = alt.Chart(df).mark_bar().encode(
        x = alt.X('Station_name',sort='-y'),
        y = 'CountOfUse',
        tooltip = [ 'Station_name','CountOfUse' ]
    ).interactive()
    
    st.subheader('Active')
    st.write('Stations with more than 434 times of use')
    st.altair_chart(chart2, use_container_width=True)




    
   
elif page == '2. The Most frequent stations':
    st.title('Top 10 frequent stations')
    st.write('identifikujte nejfrekventovanější stanice')
    st.write('Jedná sa o 10 najpoužívanejších staníc s najvačšim počtom vypujček + vrátení kol')
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
            ORDER BY countStartStation DESC
        ) SELECT start_station_name AS Station_name, (countStartStation + countEndStation ) AS CountOfUse FROM Bikes LIMIT 10

    """
    col1,col2 = st.columns([0.25,0.75])
    df = pd.read_sql(sql=query,con=engeto_data_conn)
    col1.dataframe(df,1000,300)

    
    chart1 = alt.Chart(df).mark_bar().encode(
        x = alt.X('Station_name', sort='-y'),
        y = alt.Y('CountOfUse'),
        tooltip = [ 'Station_name','CountOfUse' ]
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
   ).interactive()

    col2.altair_chart(chart1, use_container_width=True)

elif page == '3. Count of Bikes':
    st.title('Count of Bikes at stations')
    st.write('identifikujte stanice, na kterých se kola hromadí a stanice, kde potenciálně chybí')
    

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
        WHERE (countEndStation - countStartStation ) < (-1000)
        ORDER BY CountOfUse 
        
    """
    
    df = pd.read_sql(sql=query,con=engeto_data_conn)
   

    chart1 = alt.Chart(df).mark_bar().encode(
        x = alt.X('Station_name',sort='y'),
        y = 'CountOfUse',
        tooltip = [ 'Station_name','CountOfUse' ]
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
        WHERE (countEndStation - countStartStation ) > 1000
        ORDER BY CountOfUse DESC
    """
    
    df = pd.read_sql(sql=query1,con=engeto_data_conn)
   

    chart2 = alt.Chart(df).mark_bar().encode(
        x = alt.X('Station_name',sort='-y'),
        y = 'CountOfUse',
        tooltip = [ 'Station_name','CountOfUse' ]
    ).interactive()

    st.subheader ('Stations with too many bikes')
    st.write('Stations where people more end their rents than start rent of bike in the station')
    st.altair_chart(chart2, use_container_width=True)






elif page == '4. Distances between stations':
    st.title('Distances between stations')
    st.write('Spočítejte vzdálenosti mezi jednotlivými stanicemi')

    st.write('Vzdialenosť v KM medzi jednotlivými stanicami')
    
    from itertools import combinations
    from geopy.distance import geodesic
    import numpy as np
    import matplotlib

  
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
    dist_df = pd.DataFrame(distances, index=pd.Index(combos, names=['Station1', 'Station2']), columns=['distance'])
    dist_df = dist_df.join(df.rename_axis('Station1')).join(df.rename_axis('Station2'), rsuffix='2')

    
    dist_df.to_csv('your.csv', index=False)
    df = pd.read_csv('your.csv', index_col=0)
    df = df.reset_index()
    df = df[['distance','station_name','station_name2']]
    df = pd.pivot_table(df, index="station_name",
                        columns="station_name2", 
                        values="distance", fill_value=0)
    df


elif page == '5. Bike rental time':
    st.title('Bike rental time')
    st.write('Jak dlouho trvá jedna výpůjčka? Najděte odlehlé hodnoty, zobrazte histogram')

    st.write('Na základe dostupných dat možeme povedať, že :')

    student_conn_string = "mysql+pymysql://student2:eh2BjVEpYmDcT96E@data.engeto.com:3306/data_academy_02_2022"
    engeto_data_conn = sqlalchemy.create_engine(student_conn_string)


    query2="""
        SELECT duration
        FROM edinburgh_bikes eb 
    """

    df = pd.read_sql(sql=query2,con=engeto_data_conn)
    
    df = pd.DataFrame(df) 

    df = (df.describe()/60).round(1)
    df

    st.write('- Priemerna doba vypujčky je :', df['duration'].iloc[1], 'minut.')
    st.write('- 25% percentil :', df['duration'].iloc[4], 'minut.')
    st.write('- 50% percentil :', df['duration'].iloc[5], 'minut.')
    st.write('- 75% percentil :', df['duration'].iloc[6], 'minut.')
    st.write('- Variačni koeficient:', (df['duration'].iloc[2]/df['duration'].iloc[1]*100).round(0), '%.')
    st.write('- Minimálna doba vypujčky :', df['duration'].iloc[3], 'minut.')
    st.write('- Maximalna doba vypujčky :', df['duration'].iloc[7], 'minut.')



    query="""
        WITH duration AS (
        SELECT start_station_name,end_station_name, ROUND(duration/60,0) AS duration_min, CASE 
            WHEN ROUND(duration/60,0) <=10 THEN '<=10min'
            WHEN ROUND(duration/60,0) >10 AND ROUND(duration/60,0) <=19 THEN '<=19min_AND_>10min'
            WHEN ROUND(duration/60,0) >19 AND  ROUND(duration/60,0) <=42 THEN '<=42_AND_>19min'
            WHEN ROUND(duration/60,0) >42 THEN '>42min'
        END AS duration_type
        FROM edinburgh_bikes eb 
        )SELECT duration_type,COUNT(duration_type) as count
        FROM duration
        GROUP BY duration_type 
    """
    df = pd.read_sql(sql=query,con=engeto_data_conn)


    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('duration_type'),
        y = alt.Y('count'),
        tooltip = [ 'duration_type','count' ]
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
   ).interactive()

    st.altair_chart(hist, use_container_width=True)



    




elif page == 'Demand analysis':
    st.title('Development of Bike rent over time')
    st.write('- zobrazte vývoj poptávky po půjčování kol v čase')
    
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
        y = alt.Y('countOfRents'),
        tooltip = [ 'time','countOfRents' ]
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle=0
    ).interactive()
    

    st.write('The most frequent time is from 12:00 to 17:00 during the DAY')
    st.write('The lowest frequent time is from 22:00 to 06:00 during the NIGHT and EARLY MORNING')
    st.altair_chart(hist, use_container_width=True)

    st.write('- půjčují si lidé kola více o víkendu než během pracovního týdne')
    col1,col2 =st.columns(2)
    with col1:
        st.title('Bike rent during the WORKING DAYS')
        

        queryWork="""
                WITH workingdays AS (
                    SELECT WEEKDAY(started_at) AS dayInWeek,started_at 
                    FROM edinburgh_bikes eb 
                    WHERE WEEKDAY(started_at) IN ('0','1','2','3','4')
                ) SELECT count(dayInWeek)/5 as Average_Count FROM workingdays 
            """
        dfWork = pd.read_sql(sql=queryWork,con=engeto_data_conn)
        dfWork = pd.DataFrame(dfWork)

        a1 = dfWork.to_string(header=False, index=False)

        st.write('Average count of rent per day during the working days:', a1)
        
        


    with col2:
        st.title('Bike rent during the WEEKEND')
        

        queryWeek="""
        WITH weekend AS (
            SELECT WEEKDAY(started_at) AS dayInWeek,started_at  
            FROM edinburgh_bikes eb 
            WHERE WEEKDAY(started_at) IN ('5','6')
        ) SELECT count(dayInWeek)/2 AS Average_Count FROM weekend
        """
        dfWeek = pd.read_sql(sql=queryWeek,con=engeto_data_conn)
        dfWeek = pd.DataFrame(dfWeek)

        a2 = dfWeek.to_string(header=False, index=False)
        st.write('Average count of rent per day during the weekend:', a2)

    st.markdown("<h3 style='text-align: center; color: grey;'>People usually use bikes during the weekend, people use bikes 8 874,7 more then during the working days</h3>", unsafe_allow_html=True)


    st.write('- zjistěte vliv počasí na poptávku po kolech')
    col1,col2 =st.columns(2)
    with col1:
        st.title('Effect of weather on bike rent in SUMMER')

        querySummer="""
            WITH  feels_temperature AS (

                SELECT distinct AVG(feels) as feel_temperature,date
                FROM edinburgh_weather ew 
                WHERE time in ('15:00','18:00')
                GROUP BY date
                
            ),
            countOfBikes AS (

                SELECT LEFT(started_at,10) AS date ,SUBSTRING(started_at,12,2) AS time FROM edinburgh_bikes eb 
                WHERE LEFT(RIGHT(started_at,8),2) IN ('15','16','17')
                
            ), temp_bikes AS (

                SELECT COUNT(time) AS CountOfBikes, b.date, t.feel_temperature, 
                CASE
                    WHEN feel_temperature <=12 THEN 'cold <= 12 °c'
                    WHEN feel_temperature <=22 AND feel_temperature > 12 THEN 'warm > 12 °c'
                    WHEN feel_temperature >22 THEN 'hot > 22 °c'
                END AS temperature_group 
                FROM countOfBikes b
                JOIN feels_temperature t
                ON b.date=t.date
                WHERE SUBSTRING(t.date,6,2) IN ('06','07','08')
                GROUP BY date
                
            ) select AVG(CountOfBikes) as AVG_CountOfBikes, temperature_group  from temp_bikes 
            group by temperature_group 
        """

        df = pd.read_sql(sql=querySummer,con=engeto_data_conn)


        hist = alt.Chart(df).mark_bar().encode(
            x = alt.X('temperature_group'),
            y = alt.Y('AVG_CountOfBikes'),
            tooltip = [ 'temperature_group', 'AVG_CountOfBikes' ]
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle=0
        ).interactive()

        st.altair_chart(hist, use_container_width=True)

    with col2:
        st.title('Effect of weather on bike rent in WINTER')

        queryWinter="""
            WITH  feels_temperature AS (

                SELECT distinct AVG(feels) AS feel_temperature,date
                FROM edinburgh_weather ew 
                WHERE time in ('15:00','18:00')
                GROUP BY date
            
            ),
            countOfBikes AS (

                SELECT LEFT(started_at,10) AS date ,SUBSTRING(started_at,12,2) AS time FROM edinburgh_bikes eb 
                WHERE LEFT(RIGHT(started_at,8),2) IN ('15','16','17')
            
             ), temp_bikes AS (

                SELECT COUNT(time) AS CountOfBikes, b.date, t.feel_temperature, 
                CASE
                    WHEN feel_temperature <=0 THEN 'cold <= 0 °c'
                    WHEN feel_temperature <=5 AND feel_temperature > 0 THEN 'warm > 0 °c'
                    WHEN feel_temperature >5 THEN 'hot > 5 °c'
                END AS temperature_group 
                FROM countOfBikes b
                JOIN feels_temperature t
                ON b.date=t.date
                WHERE SUBSTRING(t.date,6,2) IN ('12','01','02')
                GROUP BY date
            
            ) SELECT AVG(CountOfBikes) as AVG_CountOfBikes, temperature_group  
            FROM temp_bikes 
            GROUP BY temperature_group 
        """

    
        df = pd.read_sql(sql=queryWinter,con=engeto_data_conn)


        hist = alt.Chart(df).mark_bar().encode(
            x = alt.X('temperature_group'),
            y = alt.Y('AVG_CountOfBikes'),
            tooltip = [ 'temperature_group', 'AVG_CountOfBikes' ]
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle=0
        ).interactive()

        st.altair_chart(hist, use_container_width=True)

    st.markdown("<h3 style='text-align: center; color: grey;'>People usually use bikes at the summer when the feeled temperature is high. In winter people use bikes not depend on the feeled temperature. </h3>", unsafe_allow_html=True)
        
