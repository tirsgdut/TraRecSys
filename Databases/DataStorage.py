import pymysql.cursors  #请求
import pymysql

class MySQLCommand(object):
    def __init__(self, user='root', passwords = '550909'):  #连接数据库
        self.config = {
            'host': "localhost",
            'user': user,
            'password': passwords,
            'db': 'TraRecSys',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        try:
            self.db = pymysql.connect(**self.config)
            self.cursor = self.db.cursor()
        except:
            print("connect mysql error.")



    #存储站点信息
    def subway_stations(self, dataSet):
        """
                        存入地铁相关数据的函数
                        :param dataSet:  ['station_name', 'next_stations', lon, lat]
                        其中station_uid是浮点数next_station = '{ '地铁站的id': 号线（int）, 'id':号线，}，  lon，lat为浮点数，  start_time等为时间变量
                        :return:
        """
        try:
            sqlExit = "SELECT station_name FROM subway_stations WHERE station_name = '%s'" % (dataSet[0])  # 检查导入的站点数据否存在相同的站点
            res = self.cursor.execute(sqlExit)
        except pymysql.Error as e:
            print("检查相同的站点时错误")
            return 0
        if res == 1:
            try:
                with self.db.cursor() as cursor:
                    sql = "SELECT next_stations FROM subway_stations WHERE station_name = '%s'" % (dataSet[0])   #提取到下一站信息
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    result = result[0]['next_stations'].replace("'",'"')
                    result = eval(result)     #转化为字典
                try:
                    if result.keys() != dataSet[1].keys():  # 判断两个字典相不相等
                        next_stations = {**result, **dataSet[1]}  # 两个字典拼接
                        try:
                            sql = 'UPDATE subway_stations SET next_stations = "%s" WHERE  station_name = "%s" ;' % (str(next_stations), dataSet[0])  # 更新下一站信息
                            print(sql)
                            try:
                                result = self.cursor.execute(sql)
                                self.db.commit()
                            except pymysql.Error as e:
                                # 回滚
                                self.db.rollback()
                                print("出错", e)
                        except pymysql.Error as e:
                            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
                except AttributeError:
                    if result == None:
                        next_stations = dataSet[1]
                    elif dataSet[1] == None:
                        next_stations = result
                    try:
                        sql = 'UPDATE subway_stations SET next_stations = "%s" WHERE  station_name = "%s" ;' % (
                        str(next_stations), dataSet[0])  # 更新下一站信息
                        print(sql)
                        try:
                            result = self.cursor.execute(sql)
                            self.db.commit()
                        except pymysql.Error as e:
                            # 回滚
                            self.db.rollback()
                            print("出错", e)
                    except pymysql.Error as e:
                        print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            except pymysql.Error as e:
                print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            return 0
        try:
            sql = 'INSERT INTO subway_stations(station_name, next_stations, lon, lat) VALUES ("{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    #存入算法数据库
    def subway_edges(self, dataSet):
        """
        存入地铁算法相关的数据库
        :param dataSet: [start_id, end_id, weight, line]
        :return: start_id  当前站点的uid； end_id  结尾站点的uid, weight为1， line当前所属的号线
        """
        try:
            sql = 'INSERT INTO subway_edges(now_station, next_station, weight, line) VALUES ("{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    #地铁属性
    def subway_feature(self, dataSet):
        # 地铁属性操作
        """
        start_id 起始站点， end_id终点站点, price价格, wait_time大约等待时间,
        :param dataSet:
        :return:
        """
        try:
            sql = 'INSERT INTO subwayfeature_line(start_name, end_name, wait_time,  work_endtime, line) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3], dataSet[4])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))


#存储站点信息
    def bus_stations(self, dataSet):
        """
                        存入地铁相关数据的函数
                        :param dataSet:  ['station_name', 'next_stations', lon, lat]
                        其中station_uid是浮点数next_station = '{ '地铁站的id': 号线（int）, 'id':号线，}，  lon，lat为浮点数，  start_time等为时间变量
                        :return:
        """
        try:
            sqlExit = "SELECT station_name FROM bus_stations WHERE station_name = '%s'" % (dataSet[0])  # 检查导入的站点数据否存在相同的站点
            res = self.cursor.execute(sqlExit)
        except pymysql.Error as e:
            print("检查相同的站点时错误")
            return 0
        if res == 1:
            try:
                with self.db.cursor() as cursor:
                    sql = "SELECT next_stations FROM bus_stations WHERE station_name = '%s'" % (dataSet[0])   #提取到下一站信息
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    result = result[0]['next_stations'].replace("'",'"')
                    result = eval(result)     #转化为字典
                try:
                    if result.keys() != dataSet[1].keys():  # 判断两个字典相不相等
                        next_stations = {**result, **dataSet[1]}  # 两个字典拼接
                        try:
                            sql = 'UPDATE bus_stations SET next_stations = "%s" WHERE  station_name = "%s" ;' % (str(next_stations), dataSet[0])  # 更新下一站信息
                            print(sql)
                            try:
                                result = self.cursor.execute(sql)
                                self.db.commit()
                            except pymysql.Error as e:
                                # 回滚
                                self.db.rollback()
                                print("出错", e)
                        except pymysql.Error as e:
                            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
                except AttributeError:
                    if result == None:
                        next_stations = dataSet[1]
                    elif dataSet[1] == None:
                        next_stations = result
                    try:
                        sql = 'UPDATE bus_stations SET next_stations = "%s" WHERE  station_name = "%s" ;' % (str(next_stations), dataSet[0])  # 更新下一站信息
                        print(sql)
                        try:
                            result = self.cursor.execute(sql)
                            self.db.commit()
                        except pymysql.Error as e:
                            # 回滚
                            self.db.rollback()
                            print("出错", e)
                    except pymysql.Error as e:
                        print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            except pymysql.Error as e:
                print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            return 0
        try:
            sql = 'INSERT INTO bus_stations(station_name, next_stations, lon, lat, line) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3], dataSet[4])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

 #存入算法数据库
    def bus_edges(self, dataSet):
        """
        存入地铁算法相关的数据库
        :param dataSet: [start_id, end_id, weight, line]
        :return: start_id  当前站点的uid； end_id  结尾站点的uid, weight为1， line当前所属的号线
        """
        try:
            sql = 'INSERT INTO bus_edges(now_station, next_station, weight, line) VALUES ("{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

 #地铁属性
    def bus_feature(self, dataSet):
        # 地铁属性操作
        """
        start_id 起始站点， end_id终点站点, price价格, wait_time大约等待时间,
        :param dataSet:
        :return:
        """
        try:
            sql = 'INSERT INTO busfeature_line(start_name, end_name, wait_time,  end_time, line) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(dataSet[0], dataSet[1], dataSet[2], dataSet[3], dataSet[4])
            try:
                result = self.cursor.execute(sql)
                self.db.commit()
            except pymysql.Error as e:
                # 回滚
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已经存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

# b = ['东山总站(署前路)', '芳村花园总站', '约4-10分钟/趟', '22:30', '1路(东山总站(署前路)-芳村花园总站)']
#
# a = MySQLCommand()
# a.bus_feature(b)