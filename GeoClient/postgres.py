from sshtunnel import SSHTunnelForwarder  # Run pip install sshtunnel
from sqlalchemy.orm import sessionmaker  # Run pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import inspect

def connector():
    with SSHTunnelForwarder(
        ('35.246.227.120', 22),  # Remote server IP and SSH port
        ssh_username="serap",
        ssh_password="password",
        ssh_pkey="peng",
        ssh_private_key_password="peng",
        remote_bind_address=(
        'localhost', 5432)) as server:  # PostgreSQL server IP and sever port on remote machine

        server.start()  # start ssh sever
        print('Server connected via SSH')

        # connect to PostgreSQL
        local_port = str(server.local_bind_port)
        engine = create_engine('postgresql://postgres:password@127.0.0.1:' + local_port + '/peng')
        insp = inspect(engine)
        print(insp.get_table_names())
        Session = sessionmaker(bind=engine)
        session = Session()
        test = session.execute(text("select activate_python_venv('/home/y_voigt/.venv');"))
        #test3 = session.execute(text("SELECT ST_AsText(st_centroid(st_union(geom))) FROM public.online_delivery_data"))
        test3 = session.execute(text("SELECT ST_AsText(st_centroid(st_union(geo_dp_centroid(geom,0.01)))) FROM public.online_delivery_data"))
        print('Database session created')
        session.close()

        return get_centroid(test3.fetchone())


def connectorII():
    with SSHTunnelForwarder(
            ('35.246.227.120', 22),  # Remote server IP and SSH port
            ssh_username="serap",
            ssh_password="password",
            ssh_pkey="peng",
            ssh_private_key_password="peng",
            remote_bind_address=(
                    'localhost', 5432)) as server:  # PostgreSQL server IP and sever port on remote machine

        server.start()  # start ssh sever
        print('Server connected via SSH')

        # connect to PostgreSQL
        local_port = str(server.local_bind_port)
        engine = create_engine('postgresql://postgres:password@127.0.0.1:' + local_port + '/peng')
        insp = inspect(engine)
        print(insp.get_table_names())
        Session = sessionmaker(bind=engine)
        session = Session()
        test = session.execute(text("select activate_python_venv('/home/y_voigt/.venv');"))
        # test data retrieval
        test = session.execute(text("SELECT ST_AsText(geo_dp_centroid(geom, 20)), monthly_income, ST_Envelope(geom) FROM public.online_delivery_data"))
        print(test)
        lat = []
        long = []
        incomes = []
        for _ in test:
            row = test.fetchone()
            print(row)
            print(row[0])
            x = row[0].split(" ")
            lat.append(x[0].replace("POINT(", ""))
            long.append(x[1].replace(")", ""))
            incomes.append(row[1])
        print(lat, long)
        test2 = session.execute(text("SELECT ST_AsText(ST_Envelope(st_union(geom))) FROM public.online_delivery_data"))
        rect = get_rect(test2.fetchone())
        print("Rect", rect)
        test3 = session.execute(text("SELECT ST_AsText(st_centroid(st_union(geom))) FROM public.online_delivery_data"))
        centroid = get_centroid(test3.fetchone())
        print("Centroid", centroid)
        return lat, long, incomes, centroid, rect #centroid_lat, centroid_long, bounding_rect



def get_rect(point):
    x = point[0].split(",")
    corner_list = []
    for i in x:
        corner_list.append(i.split(" "))
    print(corner_list)

    corner_list[0][0] = corner_list[0][0].replace("POLYGON((", "")
    corner_list[3][1] = corner_list[3][1].replace(")))", "")
    return(corner_list)


def get_centroid(point):
    x = point[0].split(" ")
    return [float(x[1].replace(")", "")), float(x[0].replace("POINT(", ""))]

import plotly.graph_objects as go
import numpy as np
import scipy.ndimage as ndimage

def test_plot_static():
    from random import uniform
    from collections import Counter

    def get_point():
        # Simulating getting a random point
        longitude = uniform(-180, 180)
        latitude = uniform(-90, 90)
        return longitude, latitude

    points = [get_point() for _ in range(50000)]
    longitudes, latitudes = zip(*points)

    lon_min = min(longitudes)
    lon_max = max(longitudes)

    lat_min = min(latitudes)
    lat_max = max(latitudes)

    x = list(range(int(lon_min), int(lon_max), 1))
    y = list(range(int(lat_min), int(lat_max), 1))

    z = np.zeros((len(y), len(x)))
    print(x, y, z)

    for i in points:
        z[int(i[1]-1),int(i[0]-1)] += 1

    smoothed_z = ndimage.gaussian_filter(z, sigma=10)

    # Create a surface plot
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=smoothed_z)])

    # Customize the layout
    fig.update_layout(
        title='3D Surface Plot',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )

    # Display the plot
    fig.show()

#plot_distr()
#connector()

def plot_dist():
    from random import uniform
    from collections import Counter
    longitudes = []
    latitudes = []
    session = connector()

    for i in range(100):
        cent = connector()
        print(cent)
        longitudes.append(cent[0])
        latitudes.append(cent[1])

    print(longitudes, latitudes)
    lon_min = min(longitudes)-5
    lon_max = max(longitudes)+5

    lat_min = min(latitudes)-5
    lat_max = max(latitudes)+5

    x = list(range(int(lon_min), int(lon_max), 1))
    y = list(range(int(lat_min), int(lat_max), 1))

    z = np.zeros((len(y), len(x)))

    for i in range(len(latitudes)):
        z[int(latitudes[i]-lat_min),int(longitudes[i]-lon_min)] += 1

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
    fig.update_layout(
        title='3D Surface Plot',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )
    fig.show()

    smoothed_z = ndimage.gaussian_filter(z, sigma=1)
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=smoothed_z)])
    fig.update_layout(
        title='3D Surface Plot',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )
    fig.show()

    smoothed_z = ndimage.gaussian_filter(z, sigma=5)
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=smoothed_z)])
    fig.update_layout(
        title='3D Surface Plot',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )
    fig.show()

#plot_dist()