import sys,datetime

class TrackPoint():
  def __init__(self,lat,lon,timestamp):
    self.lat = lat
    self.lon = lon
    self.time = timestamp
  def __repr__(self):
    return "%f, %f  @ %s" % (self.lat,self.lon,self.time)
    

def _lat_lon_from_str(geo_str,num_int_digits,hemisphere):
  int_portion = int(geo_str[0:num_int_digits])
  dec_portion = float("0." + str(geo_str.replace('.','')[num_int_digits:-1]))
  num = int_portion + dec_portion
  if("S" == hemisphere or "W" == hemisphere):
    num = num * -1
  return num

def parse_log_file(log_file):
  track_points = []
  for line in log_file:
    try:
      parts = line.split(',')
      fmt = parts[0]
      if("$PMGNTRK" == fmt):
        lat_str = parts[1]
        lat_hem = parts[2]
        lon_str = parts[3]
        lon_hem = parts[4]
        time_str = parts[7]
        date_str, checksum = parts[10].split("*")
        lat = _lat_lon_from_str(lat_str,2,lat_hem)
        lon = _lat_lon_from_str(lon_str,3,lon_hem)      

        # Parse date/time information
        day,month,year = [int(date_str[0:2]),int(date_str[2:4]),int(date_str[4:6])]      
        # Thanks, garmin, for storing 2 digit years! This will break in 2090... I'm okay with that
        if(year>90):
          year += 1900
        else:
          year += 2000
        hour,minute,second = int(time_str[0:2]),int(time_str[2:4]),float(time_str[4:-1])
        timestamp = datetime.datetime(year,month,day,hour,minute,second)
        track_points.append(TrackPoint(lat,lon,timestamp))
    except Exception, e:
      print "Couln't parse line: %s" % line
      raise e
  return track_points


if __name__ == "__main__":
  input_file = open(sys.argv[1], 'r')
  points = parse_log_file(input_file)
  print len(points)
  for p in points:
    print p
  
  
def test_from_string():
  string = """$PMGNTRK,4737.428,N,12219.544,W,00101,M,100539.96,A,,091110*6E
  $PMGNTRK,4737.462,N,12219.535,W,00101,M,100549.96,A,,091110*61
  $PMGNTRK,4737.473,N,12219.541,W,00101,M,100607.56,A,,091110*67
  $PMGNCMD,END*3D"""
  
  parse_line(string)