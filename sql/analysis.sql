-- Quelles villes auront les températures les plus élevées ?
select c.city_id, c.city, w.temperature_2m_max from cities c
join weather w on c.city_id = w.city_id
order by w.temperature_2m_max desc
limit 5;

-- Quelles villes auront les plus fortes précipitations ?
select c.city_id, c.city, max(w.precipitation_sum) as plusFort_prec from cities c
join weather w on w.city_id = c.city_id
group by c.city_id, c.city
order by plusFort_prec desc
limit 5;


-- Quelles villes présentent le risque moyen le plus élevé ?
select c.city_id, c.city, avg(wf.risk_score) as moyenne_risk from cities c 
join weather w on w.city_id = c.city_id
join weather_features wf on wf.weather_id = w.weather_id
group by c.city_id, c.city
order by moyenne_risk desc
limit 5;

-- Quelles périodes présentent le risque maximal?
select w.time, max(wf.risk_score) as risk_max from weather_features wf 
join weather w on w.weather_id = wf.weather_id
group by w.time
order by risk_max desc
limit 5; 

-- Pour chaque ville, quelle période présente le plus grand risque 
-- select c.city_id, c.city, w.time, max(wf.risk_score) as risk_max from cities c
-- join weather w on w.city_id = c.city_id
-- join weather_features wf on w.weather_id = wf.weather_id
-- group by c.city_id, c.city, w.time
-- order by risk_max desc
-- limit 5;

-- select c.city_id , min(w.time) , max(w.time) 
-- from cities c
-- join weather w on w.city_id = c.city_id
-- join weather_features wf on wf.weather_id = w.weather_id
-- where wf.risk_level in ('Medium' , 'High')
-- GROUP BY c.city_id;

select c.city_id, c.city, w.time, wf.risk_score, wf.risk_level from cities c
join weather w on w.city_id = c.city_id
join weather_features wf on wf.weather_id = w.weather_id
where wf.risk_score = (
    select max(wf2.risk_score)
    from weather w2
    join weather_features wf2 on wf2.weather_id = w2.weather_id
    where w2.city_id = c.city_id
)
order by c.city_id, w.time;