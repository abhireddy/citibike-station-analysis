SELECT
  cal_day as trip_date,
  EXTRACT(DAYOFWEEK FROM cal_day) as day_of_week,
  EXTRACT(WEEK FROM cal_day) as week_of_year,
  EXTRACT(YEAR FROM cal_day) as year,
  EXTRACT(HOUR FROM starttime) as trip_start_hour,
  SUM(1) as trips

FROM UNNEST(GENERATE_DATE_ARRAY(
    (SELECT MIN(DATE(starttime)) FROM `bigquery-public-data.new_york_citibike.citibike_trips`),
    (SELECT MAX(DATE(starttime)) FROM `bigquery-public-data.new_york_citibike.citibike_trips`),
    INTERVAL 1 DAY
  )) as cal_day -- generate a complete date range to address gap in dataset

LEFT JOIN `bigquery-public-data.new_york_citibike.citibike_trips` t ON DATE(t.starttime) = cal_day

GROUP BY 1,2,3,4,5
