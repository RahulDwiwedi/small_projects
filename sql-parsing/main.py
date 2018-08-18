import string

from  moz_sql_parser import parse
import urllib
import json
import os
# from flask import Flask
# from flask import request
# from flask import make_response
# from flask_cors import CORS,cross_origin
#
#
# # Flask app should start in global layout
# app = Flask(__name__)
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
#
#
# @app.route('/sql-visualizer', methods=['POST'])
# @cross_origin()
# def webhook():
#     req = request.get_json(silent=True, force=True)
#     # req = request.get()
#     print("Request:")
#     print(json.dumps(req, indent=4))
#     # sql = req.get("sql")
#     res = json.dumps(parse(req))
#     # print (res)
#
#     r = make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     return r
#
# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#
#     print ("Starting app on port %d" %(port))
#
# app.run(debug=True, port=port, host='127.0.0.1')
#
#
#



sql1 ='''SELECT end_Date FROM indochina_tccc_prod.COKE_CALENDAR WHERE year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB() BETWEEN start_date AND DATE_SUB() LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB() BETWEEN start_date AND DATE_SUB() LIMIT 1)ORDER BY week_num desc LIMIT 1'''
sql2="SELECT DISTINCT a.order_no, CAST(b.product_id AS string) AS product_id, a.user_id, a.CUSTOMER_ID, a.sapcustomerid, b.Quantity_Confirmed, b.Quantity_Confirmed_EC, b.Confirmed_Date AS confirmed_date_lines, a.order_date, a.confirmed_date AS confirmed_date_headers FROM indochina_tccc_test.ORDER_HEADERS_BASE AS a INNER JOIN indochina_tccc_test.ORDER_LINES_BASE AS b ON a.order_no = b.order_no"
sql3 = "SELECT customerid, subgroupdesc, sum(volume) as volume_py_ytd FROM (SELECT customerid, productid, subgroupdesc, CASE WHEN cs2uc.ConversionBaseNominator IS NOT NULL AND cs2uc.ConversionBaseNumerator IS NOT NULL THEN volume * (CAST(cs2uc.ConversionBaseNominator AS float64) / CAST(cs2uc.ConversionBaseNumerator AS float64)) ELSE volume END AS volume FROM ( SELECT customerid, productid, subgroupdesc, volume FROM indochina_tccc_prod.mm_orders_2017_2018 WHERE CAST(batchdate AS date) BETWEEN ( SELECT Start_Date FROM indochina_tccc_prod.COKE_CALENDAR WHERE year = ( SELECT year-1 AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Saigon'),INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND (DATE_SUB(CURRENT_DATE('Asia/Saigon'), INTERVAL 1 day))) AS x LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2uc ON x.productid = cs2uc.materialno WHERE cs2uc.AlternateStockKeepingUnit LIKE '%UC%') group by customerid, subgroupdesc"
sql4 = "Select * from (select name,lastname from tabl1)"
sql5 = "SELECT DISTINCT ebMobile__UserCode__c AS usercode, ebMobile__VisitDuration__c, ebMobile__CallDate__c, ebMobile__AccountNumber__c, ebMobile__TimeOutOutlet__c, ebMobile__TimeInOutlet__c FROM indochina_tccc_prod.ebMobile__Call__c_BASE where ebMobile__CallDate__c like '%2018-05-09%' and ebMobile__UserCode__c= '00055357'"
sql6 = '''select * from (select * from (SELECT order_no, user_id, customer_id, date, UOM_CODE, PRICE, Quantity_Confirmed, productid, SubGroupDesc, CountryID AS country FROM ( SELECT * EXCEPT(product_id, PackType, BrandDesc) FROM ( SELECT order_no, user_id, customer_id, date, UOM_CODE, PRICE, product_id, Quantity_Confirmed FROM ( SELECT DISTINCT a.order_no, a.ordertype, a.org_id, SUBSTR(a.order_date,1,10) AS date, CAST(b.product_id AS string) AS product_id, a.user_id, a.CUSTOMER_ID, b.Quantity_Confirmed, CAST(ifnull(b.Line_Disc_Amount, b.Line_Amount) AS float64)AS price, b.UOM_CODE FROM ( SELECT DISTINCT order_no, ordertype, org_id, user_id, visit_id, CUSTOMER_ID, order_date, confirmed_date FROM `indochina_tccc_test.cleaned_order_headers` ) AS a INNER JOIN `indochina_tccc_test.cleaned_order_lines` AS b ON a.order_no = b.order_no) WHERE SUBSTR(date,1,4) ="2017") AS x LEFT JOIN ( SELECT DISTINCT b.id AS productid, PackType, SubGroupDesc, BrandDesc FROM indochina_tccc_prod.sapProduct_BASE AS a INNER JOIN `indochina_tccc_test.PRODUCTS_BASE` AS b ON a.productid=b.code ) AS d ON LTRIM(TRIM(x.product_id),'0')= CAST(d.productid AS string)) AS g INNER JOIN `indochina_tccc_test.CUSTOMERS_BASE` AS h ON h.id=g.customer_id) where country like "%MM%" ) union all SELECT Order_No, RepId, customerid, batchdate, UOM_CODE, cast(Price as float64), cast(volume as string), cast(productid as int64), subgroupdesc, Country FROM ( SELECT Order_No, RepId, k.customerid, batchdate, "CS" as UOM_CODE, productid, subgroupdesc, Price, CASE WHEN ea2csD IS NOT NULL OR ea2csN IS NOT NULL THEN (Qty_delevered_sub*(ea2csN/ea2csD)) ELSE (Qty_delevered_sub) END + CASE WHEN cs2csN IS NOT NULL OR cs2csD IS NOT NULL THEN (Qty_delevered*(cs2csN/cs2csD)) ELSE (Qty_delevered) END AS volume, Country FROM ( SELECT Order_No, RepId, batchdate, customerid, price, productid, SubGroupDesc, Qty_delevered, Qty_delevered_sub, UOM_Unit, UOM_Sub_Unit, CAST(cs2cs.ConversionBaseNominator AS float64) AS cs2csD, CAST(cs2cs.ConversionBaseNumerator AS float64) AS cs2csN, CAST(ea2cs.ConversionBaseNominator AS float64) AS ea2csD, CAST(ea2cs.ConversionBaseNumerator AS float64) AS ea2csN, CAST(cs2uc.ConversionBaseNominator AS float64) AS cs2ucD, CAST(cs2uc.ConversionBaseNumerator AS float64) AS cs2ucN, Country FROM ( SELECT Order_No, RepId, CustomerId, batchdate, UOM_Unit, UOM_Sub_Unit, Price, ArticleNumber AS productid, Qty_Delivered_Units AS Qty_delevered, Qty_Delivered_Sub_Units AS Qty_delevered_sub, Country, SubGroupDesc FROM ( SELECT * EXCEPT(ChangeDateTime, DeleteFlag, CreateDateTime) FROM ( SELECT a.*, b.* EXCEPT(order_no) FROM ( SELECT DISTINCT Order_No, RepId, CustomerId, batchdate FROM `indochina_tccc_prod.bosDeliveryDocumentHeader_BASE` WHERE UPPER(country) LIKE "MM" ) AS a LEFT JOIN `indochina_tccc_prod.bosDeliveryDocumentItem_BASE` AS b ON a.order_no = b.order_no) AS c LEFT JOIN `indochina_tccc_prod.sapProduct_BASE` AS sapProd ON sapProd.ProductId = c.articlenumber) ) AS x LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2cs ON x.productid = cs2cs.materialno AND x.UOM_Unit = cs2cs.AlternateStockKeepingUnit LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS ea2cs ON x.productid = ea2cs.materialno AND x.UOM_Sub_Unit = ea2cs.AlternateStockKeepingUnit LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2uc ON x.productid = cs2uc.materialno WHERE cs2uc.AlternateStockKeepingUnit LIKE "%UC%" ) as k)'''
sql7 = '''SELECT businesspartner AS manager_id, CONCAT(firstname,' ',lastname) AS name, a.salesorg, b.codedesc AS salesorgdesc, type AS type_, volume_value AS vol_value, revenue_value AS rev_value FROM ( SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_mtd.salesorg, sales_cy_mtd.salesorg_, 'cy_mtd' AS type, SUM(volume_cy_mtd) AS volume_value, SUM(revenue_cy_mtd) AS revenue_value FROM ( SELECT customerid, salesorg, customer.geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_mtd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_mtd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND (DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 day)) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_mtd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_mtd.customerid AND asm.salesorg=sales_cy_mtd.salesorg AND asm.salesorg_=sales_cy_mtd.salesorg_ GROUP BY businesspartner, sales_cy_mtd.salesorg, sales_cy_mtd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_ytd.salesorg, sales_cy_ytd.salesorg_, 'cy_ytd' AS type, SUM(volume_cy_ytd) AS volume_value, SUM(revenue_cy_ytd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_ytd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_ytd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN (( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE month_num=1 AND week_num=1 AND year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1))) AND (DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 day)) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_ytd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_ytd.customerid AND asm.salesorg=sales_cy_ytd.salesorg AND asm.salesorg_=sales_cy_ytd.salesorg_ GROUP BY businesspartner, sales_cy_ytd.salesorg, sales_cy_ytd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_mtd.salesorg, sales_py_mtd.salesorg_, 'py_mtd' AS type, SUM(volume_py_mtd) AS volume_value, SUM(revenue_py_mtd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_mtd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_mtd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE year = ( SELECT year-1 AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_mtd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_mtd.customerid AND asm.salesorg=sales_py_mtd.salesorg AND asm.salesorg_=sales_py_mtd.salesorg_ GROUP BY businesspartner, sales_py_mtd.salesorg, sales_py_mtd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_ytd.salesorg, sales_py_ytd.salesorg_, 'py_ytd' AS type, SUM(volume_py_ytd) AS volume_value, SUM(revenue_py_ytd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_ytd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_ytd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE month_num=1 AND week_num=1 AND year = ( SELECT year-1 AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1)) AND ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_ytd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_ytd.customerid AND asm.salesorg=sales_py_ytd.salesorg AND asm.salesorg_=sales_py_ytd.salesorg_ GROUP BY businesspartner, sales_py_ytd.salesorg, sales_py_ytd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_yesterday.salesorg, sales_cy_yesterday.salesorg_, 'cy_yesterday' AS type, SUM(volume_cy_yesterday) AS volume_value, SUM(revenue_cy_yesterday) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_yesterday, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_yesterday FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) = DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_yesterday LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_yesterday.customerid AND asm.salesorg=sales_cy_yesterday.salesorg AND asm.salesorg_=sales_cy_yesterday.salesorg_ GROUP BY businesspartner, sales_cy_yesterday.salesorg, sales_cy_yesterday.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_yesterday.salesorg, sales_py_yesterday.salesorg_, 'py_yesterday' AS type, SUM(volume_py_yesterday) AS volume_value, SUM(revenue_py_yesterday) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_yesterday, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_yesterday FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) = ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_yesterday LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_yesterday.customerid AND asm.salesorg=sales_py_yesterday.salesorg AND asm.salesorg_=sales_py_yesterday.salesorg_ GROUP BY businesspartner, sales_py_yesterday.salesorg, sales_py_yesterday.salesorg_ ) AS a LEFT JOIN ( SELECT * FROM `indochina_tccc_prod.sapCodeDesc_BASE` WHERE SalesOrg LIKE 'KH%' AND CodeCategory='GEO_CODE' ) AS b ON a.salesorg_ = b.codevalue LEFT JOIN ( SELECT DISTINCT personno, firstname, lastname FROM `indochina_tccc_prod.sapPerson_BASE` ) AS c ON a.businesspartner = c.personno'''

sql8="SELECT customerid_, geocode_code_ FROM ( SELECT customerid, geocode, ram AS rn FROM indochina_tccc_prod.sapCustomer_BASE)"
sql9=''' SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_mtd.salesorg, sales_cy_mtd.salesorg_, 'cy_mtd' AS type, SUM(volume_cy_mtd) AS volume_value, SUM(revenue_cy_mtd) AS revenue_value FROM ( SELECT customerid, salesorg, customer.geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_mtd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_mtd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND (DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 day)) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_mtd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_mtd.customerid AND asm.salesorg=sales_cy_mtd.salesorg AND asm.salesorg_=sales_cy_mtd.salesorg_ GROUP BY businesspartner, sales_cy_mtd.salesorg, sales_cy_mtd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_ytd.salesorg, sales_cy_ytd.salesorg_, 'cy_ytd' AS type, SUM(volume_cy_ytd) AS volume_value, SUM(revenue_cy_ytd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_ytd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_ytd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN (( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE month_num=1 AND week_num=1 AND year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1))) AND (DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 day)) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_ytd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_ytd.customerid AND asm.salesorg=sales_cy_ytd.salesorg AND asm.salesorg_=sales_cy_ytd.salesorg_ GROUP BY businesspartner, sales_cy_ytd.salesorg, sales_cy_ytd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_mtd.salesorg, sales_py_mtd.salesorg_, 'py_mtd' AS type, SUM(volume_py_mtd) AS volume_value, SUM(revenue_py_mtd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_mtd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_mtd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE year = ( SELECT year-1 AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_mtd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_mtd.customerid AND asm.salesorg=sales_py_mtd.salesorg AND asm.salesorg_=sales_py_mtd.salesorg_ GROUP BY businesspartner, sales_py_mtd.salesorg, sales_py_mtd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_ytd.salesorg, sales_py_ytd.salesorg_, 'py_ytd' AS type, SUM(volume_py_ytd) AS volume_value, SUM(revenue_py_ytd) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_ytd, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_ytd FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE month_num=1 AND week_num=1 AND year = ( SELECT year-1 AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1)) AND ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_ytd LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_ytd.customerid AND asm.salesorg=sales_py_ytd.salesorg AND asm.salesorg_=sales_py_ytd.salesorg_ GROUP BY businesspartner, sales_py_ytd.salesorg, sales_py_ytd.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_cy_yesterday.salesorg, sales_cy_yesterday.salesorg_, 'cy_yesterday' AS type, SUM(volume_cy_yesterday) AS volume_value, SUM(revenue_cy_yesterday) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_cy_yesterday, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_cy_yesterday FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) = DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_cy_yesterday LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_cy_yesterday.customerid AND asm.salesorg=sales_cy_yesterday.salesorg AND asm.salesorg_=sales_cy_yesterday.salesorg_ GROUP BY businesspartner, sales_cy_yesterday.salesorg, sales_cy_yesterday.salesorg_ UNION ALL SELECT (CASE WHEN businesspartner IS NULL THEN 'NA' ELSE businesspartner END) AS businesspartner, sales_py_yesterday.salesorg, sales_py_yesterday.salesorg_, 'py_yesterday' AS type, SUM(volume_py_yesterday) AS volume_value, SUM(revenue_py_yesterday) AS revenue_value FROM ( SELECT customerid, salesorg, geocode AS salesorg_, SUM(CAST(qtyuom2 AS float64)) AS volume_py_yesterday, SUM( CAST( GrossRevenue AS float64 ))+ SUM( CAST( transportallowance AS float64 ))- SUM( CAST( disctradedisc AS float64 ))- SUM( CAST( disctraderegion AS float64 ))- SUM( CAST( discpromotional AS float64 ))- SUM( CAST( discfreecases AS float64 ))- SUM( CAST( discrebates AS float64 ))- SUM( CAST( discdistdisc AS float64 ))- SUM( CAST( disceveryday AS float64 ))- SUM( CAST( discincentives AS float64 ))- SUM( CAST( discpromregion AS float64 )) AS revenue_py_yesterday FROM `indochina_tccc_prod.sapSales_BASE` AS sales INNER JOIN ( SELECT cust.customerid AS cust_id, geocode FROM ( SELECT customerid, geocode FROM ( SELECT customerid, geocode, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY CAST(SUBSTR(changedatetime,1,10) AS date )) AS rn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE rn=1) AS cust ) AS customer ON TRIM(sales.customerid)=TRIM(customer.cust_id) WHERE DATE( CAST( SUBSTR( postingdate, 1, 4 ) AS int64 ), CAST( SUBSTR( postingdate, 6, 2 ) AS int64 ), CAST( SUBSTR( postingdate, 9, 2 ) AS int64 ) ) = ( SELECT DATE_ADD(a.start_date,INTERVAL b.day_of_week day) AS lastyear_date FROM indochina_tccc_prod.COKE_CALENDAR AS a INNER JOIN ( SELECT start_date, year, week_num, DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), DATE_DIFF(DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY), start_date, day) AS day_of_week FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Phnom_Penh'), INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 DAY)) AS b ON (a.year+1)=b.year AND a.week_num=b.week_num) AND SalesOrg LIKE 'KH%' GROUP BY customerid, salesorg, salesorg_) AS sales_py_yesterday LEFT JOIN ( SELECT businesspartner, customerid, salesorg, geocode AS salesorg_ FROM ( SELECT DISTINCT businesspartner, customerno FROM `indochina_tccc_prod.sapPartnerFunction_BASE` WHERE partnerfunctiontext = 'ASM')AS a INNER JOIN ( SELECT * FROM ( SELECT *, ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY DATE(CAST(SUBSTR(changedatetime, 1, 4 ) AS int64 ), CAST( SUBSTR( changedatetime, 6, 2 ) AS int64 ), CAST( SUBSTR( changedatetime, 9, 2 ) AS int64 ) ) DESC) AS cn FROM `indochina_tccc_prod.sapCustomer_BASE`) WHERE cn=1 AND salesorg LIKE 'KH%') AS b ON a.businesspartner=b.managerid AND a.customerno=b.customerid ) AS asm ON asm.customerid = sales_py_yesterday.customerid AND asm.salesorg=sales_py_yesterday.salesorg AND asm.salesorg_=sales_py_yesterday.salesorg_ GROUP BY businesspartner, sales_py_yesterday.salesorg, sales_py_yesterday.salesorg_ '''


sql10='''select * from (select a.*,substr(f.region,1,2) as country from (SELECT ebMobile__CallDate__c, calldate, ebMobile__UserCode__c as usercode, cast(ebMobile__VisitDuration__c as float64) as duration, ebMobile__TimeInOutlet__c, ebMobile__TimeOutOutlet__c, ebMobile__CallType__c, ebMobile__OffRouteFlag__c FROM `indochina_tccc_prod.ebMobile__Call__c_BASE` WHERE EXTRACT(dayofweek FROM CAST(SUBSTR(calldate ,1,10) AS date)) = 1 AND SUBSTR(calldate ,1,10) LIKE "%2018-06%" and ebMobile__OffRouteFlag__c is False) as a LEFT JOIN indochina_tccc_prod.sapPerson_BASE AS f ON f.personno=a.usercode ) where duration=506.58'''




sql11="select * from ram"
sql12='''SELECT customerid, productid, subgroupdesc, volume_cy_mtd FROM ( SELECT customerid, productid, subgroupdesc, CASE WHEN ea2csD IS NOT NULL OR ea2csN IS NOT NULL THEN (Qty_delevered_sub*(ea2csN/ea2csD))*(cs2ucD/cs2ucN) ELSE (Qty_delevered_sub)*(cs2ucD/cs2ucN) END + CASE WHEN cs2csN IS NOT NULL OR cs2csD IS NOT NULL THEN (Qty_delevered*(cs2csN/cs2csD))*(cs2ucD/cs2ucN) ELSE (Qty_delevered)*(cs2ucD/cs2ucN) END AS volume_cy_mtd FROM ( SELECT customerid, productid, SubGroupDesc, Qty_delevered, Qty_delevered_sub, UOM_Unit, UOM_Sub_Unit, CAST(cs2cs.ConversionBaseNominator AS float64) AS cs2csD, CAST(cs2cs.ConversionBaseNumerator AS float64) AS cs2csN, CAST(ea2cs.ConversionBaseNominator AS float64) AS ea2csD, CAST(ea2cs.ConversionBaseNumerator AS float64) AS ea2csN, CAST(cs2uc.ConversionBaseNominator AS float64) AS cs2ucD, CAST(cs2uc.ConversionBaseNumerator AS float64) AS cs2ucN FROM ( SELECT customerid, productid, SubGroupDesc, SUM(CAST(Qty_Delivered_Units AS float64)) AS Qty_delevered, SUM(CAST( Qty_Delivered_Sub_Units AS float64)) AS Qty_delevered_sub, UOM_Unit, UOM_Sub_Unit FROM ( SELECT * EXCEPT(ChangeDateTime, DeleteFlag, CreateDateTime) FROM ( SELECT a.*, b.* EXCEPT(order_no) FROM ( SELECT DISTINCT Order_No, RepId, CustomerId, DeliveryDate FROM `indochina_tccc_prod.bosDeliveryDocumentHeader_BASE` WHERE UPPER(country) LIKE "MM" ) AS a LEFT JOIN `indochina_tccc_prod.bosDeliveryDocumentItem_BASE` AS b ON a.order_no = b.order_no) AS c LEFT JOIN `indochina_tccc_prod.sapProduct_BASE` AS sapProd ON sapProd.ProductId = c.articlenumber) WHERE CAST(deliverydate AS date) BETWEEN ( SELECT Start_Date FROM `indochina_tccc_prod.COKE_CALENDAR` WHERE year = ( SELECT year AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Saigon'),INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) AND month = ( SELECT month AS mn FROM indochina_tccc_prod.COKE_CALENDAR WHERE DATE_SUB(CURRENT_DATE('Asia/Saigon'),INTERVAL 1 DAY) BETWEEN start_date AND DATE_SUB(end_date, INTERVAL 1 day) LIMIT 1) ORDER BY week_num LIMIT 1) AND (DATE_SUB(CURRENT_DATE('Asia/Saigon'), INTERVAL 1 day)) AND SubGroupDesc IS NOT NULL GROUP BY SubGroupDesc, customerid, productid, UOM_Unit, UOM_Sub_Unit) AS x LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2cs ON x.productid = cs2cs.materialno AND x.UOM_Unit = cs2cs.AlternateStockKeepingUnit LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS ea2cs ON x.productid = ea2cs.materialno AND x.UOM_Sub_Unit = ea2cs.AlternateStockKeepingUnit LEFT JOIN indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2uc ON x.productid = cs2uc.materialno WHERE cs2uc.AlternateStockKeepingUnit LIKE "%UC%" ))'''


sql13='''SELECT
  customerid,
  SubGroupDesc,
  SUM(CAST(Price AS float64)) as revenue_cy_ytd
FROM (
  SELECT
    * EXCEPT(ChangeDateTime,
      DeleteFlag,
      CreateDateTime)
  FROM (
    SELECT
      a.*,
      b.* EXCEPT(order_no)
    FROM (
      SELECT
        DISTINCT Order_No,
        RepId,
        CustomerId,
        DeliveryDate
      FROM
        `indochina_tccc_prod.bosDeliveryDocumentHeader_BASE`
      WHERE
        UPPER(country) LIKE "MM" ) AS a
    LEFT JOIN
      `indochina_tccc_prod.bosDeliveryDocumentItem_BASE` AS b
    ON
      a.order_no = b.order_no) AS c
  LEFT JOIN
    `indochina_tccc_prod.sapProduct_BASE` AS sapProd
  ON
    sapProd.ProductId = c.articlenumber)
    where cast(deliverydate as date) BETWEEN (
SELECT
Start_Date
FROM
`indochina_tccc_prod.COKE_CALENDAR`
WHERE
year = (
SELECT
year AS mn
FROM
indochina_tccc_prod.COKE_CALENDAR
WHERE
DATE_SUB(CURRENT_DATE('Asia/Saigon'),INTERVAL 1 DAY) BETWEEN start_date
AND DATE_SUB(end_date, INTERVAL 1 day)
LIMIT
1)

ORDER BY
week_num
LIMIT
1)
AND (DATE_SUB(CURRENT_DATE('Asia/Saigon'), INTERVAL 1 day))
and SubGroupDesc is not null
GROUP BY
  SubGroupDesc,
  customerid'''



def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
    return results


sql14='''SELECT
  a.customer_id AS customer_id_,
  a.customer_code AS customer_id,
  a.salesorg,
  a.customertype,
  b.order_no,
  b.Confirmed_Date,
  b.Quantity_Confirmed,
  b.Quantity_Confirmed_EC,
  b.volume_uc,
  b.total_amount,
  b.unit_price,
  b.PRODUCT_ID,
  b.subgroupdesc,
  a.street,
  a.city,
  a.customername,
  a.longitude,
  a.latitude,
  a.tradechannel,
  a.Classification,
  a.sapcustomerid,
  salesorgdesc_.salesorgdesc AS salesorg_,
  g.codedesc AS tradechannel_,
  h.codedesc AS customertype_,
  a.repid AS personno,
  i.firstname AS firstname_bkp,
  i.lastname AS lastname_bkp,
   a.first_name_ AS firstname,
   a.last_name_ AS lastname,
  CONCAT(firstname, " ", lastname) AS name,
  j.codedesc AS outlet_class,
  a.province AS province
FROM (
  SELECT
    *
  FROM (
    SELECT
      a.customer_id,
      c.code AS customer_code,
      b.salesorg,
      customertype,
      b.street,
      b.city,
      c.name AS customername,
      c.province as province,
      b.longitude,
      b.latitude,
      b.tradechannel,
      b.Classification,
      b.customerid AS sapcustomerid,
      user.Code AS repid,
      user.First_Name AS first_name_,
      user.laster_name AS last_name_,
      b.region,
      ROW_NUMBER() OVER(PARTITION BY a.customer_id ORDER BY changedatetime DESC) AS rn
    FROM (
      SELECT
        *
      FROM (
        SELECT
          customer_id,
          user_id,
          ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY confirmed_date DESC) AS rn_
        FROM
          `indochina_tccc_test.ORDER_HEADERS_*`
         WHERE
           CAST(SUBSTR(confirmed_date,1,4) AS int64) >= 2017
    )
      WHERE
        rn_=1) AS a
    INNER JOIN
      (
  SELECT
    b.id,
    b.name,
    b.code,
    b.Distrib,
    salesorg,
    region AS region_is_province_code,
    province
  FROM (
    SELECT
      *
    FROM (
      SELECT
        id,
        Distrib,
        name,
        code,
        ROW_NUMBER() OVER(PARTITION BY id ORDER BY CAST(SUBSTR(REC_TIME_STAMP,1,10)AS date)) AS rn
      FROM
        indochina_tccc_test.vwCUSTOMERS_BASE
      WHERE
        TRIM(Company) LIKE 'V%')
    WHERE
      rn=1) AS b
  INNER JOIN (
    SELECT
      DISTINCT customerid AS id,
      x.salesorg,
      y.SalesOrgDesc,
      region,
      codedesc AS province
    FROM (
      SELECT
        *
      FROM (
        SELECT
          *,
          ROW_NUMBER() OVER(PARTITION BY customerid ORDER BY changedatetime) AS rn
        FROM
          `indochina_tccc_prod.sapCustomer_BASE`)
      WHERE
        rn=1 ) AS x
      INNER JOIN
        `indochina_tccc_prod.sapSalesOrg_BASE` AS y
      ON
        TRIM(x.salesorg)=(y.SalesOrg)
      INNER JOIN (
        SELECT
          DISTINCT codevalue,
          codedesc
        FROM
          `indochina_tccc_prod.sapCodeDesc_BASE`
        WHERE
          codecategory='REGION'
          AND salesorg LIKE 'VN%') AS z
      ON
        TRIM(x.region)=TRIM(z.codevalue) ) AS a
    ON
      TRIM(a.id)=TRIM(b.Distrib)) AS c
    ON
      a.CUSTOMER_ID = c.id
    left JOIN
      `indochina_tccc_prod.sapCustomer_BASE` AS b
    ON
      c.CODE = b.customerid
    left join(select distinct user_id,Code,First_Name,Laster_Name from `indochina_tccc_test.Users_BASE` ) as user
    on a.user_id=user.user_id
    WHERE
      b.customertype NOT IN ('01',
        '04',
        '05',
        '06',
        '13')

     )
  WHERE
    rn = 1) AS a
LEFT JOIN (
  SELECT
    a.order_no,
    CAST(IFNULL(b.Line_Disc_Amount,
        b.Line_Amount) AS float64)AS total_amount,
    b.unit_price,
    customer_id,
    a.Confirmed_Date,
    (CASE a.OrderType
        WHEN 0 THEN IFNULL(CAST(b.Quantity_Confirmed AS float64),  0)
        ELSE IFNULL(-CAST(b.Quantity_Confirmed AS float64),
        0) END) AS Quantity_Confirmed,
    (CASE a.OrderType
        WHEN 0 THEN IFNULL(CAST(b.Quantity_Confirmed_ec AS float64),  0)
        ELSE IFNULL(-CAST(b.Quantity_Confirmed_ec AS float64),
        0) END) AS Quantity_Confirmed_EC,
    CAST(ConversionBaseNominator AS float64) * (CASE a.OrderType
        WHEN 0 THEN IFNULL(CAST(b.Quantity_Confirmed AS float64),  0)
        ELSE IFNULL(-CAST(b.Quantity_Confirmed AS float64),
        0) END)/CAST(ConversionBaseNumerator AS float64) AS volume_uc,
    d.PRODUCT_ID,
    d.subgroupdesc
  FROM (
    SELECT
      DISTINCT USER_ID,
      order_no,
      customer_id,
      OrderType,
      confirmed_date
    FROM
      `indochina_tccc_test.ORDER_HEADERS_*`
    WHERE
      CAST(STATUS AS int64)=6 ) AS a
  INNER JOIN
    `indochina_tccc_test.ORDER_LINES_BASE` AS b
  ON
    a.order_no = b.order_no
  LEFT JOIN
    `indochina_tccc_prod.sapMaterialConversionRate_BASE` AS c
  ON
    b.PRODUCT_CODE = c.MaterialNo
  LEFT JOIN (
    SELECT
      DISTINCT id AS product_id,
      subgroupdesc
    FROM
      `indochina_tccc_test.PRODUCTS_BASE` AS x
    INNER JOIN
      `indochina_tccc_prod.sapProduct_BASE` AS y
    ON
      x.code = y.productid ) AS d
  ON
    b.product_id = d.product_id
  WHERE
    c.AlternateStockKeepingUnit = 'UC'
    AND CAST(SUBSTR(b.confirmed_date,1,4) AS int64) >= 2017
    AND CAST(b.OrderLineStatus AS int64)=2
    AND IFNULL(CAST(b.FREE_PRODUCTS AS int64),
      0)<>1 ) AS b
ON
  a.customer_id = b.customer_id
LEFT JOIN (
  SELECT
    DISTINCT SalesOrgDesc,
    salesorg
  FROM
    `indochina_tccc_prod.sapSalesOrg_BASE` ) AS salesorgdesc_
ON
  a.salesorg = salesorgdesc_.salesorg
LEFT JOIN (
  SELECT
    CodeDesc,
    CodeValue,
    SalesOrg,
    CountryId
  FROM
    indochina_tccc_prod.sapCodeDesc_BASE
  WHERE
    UPPER(CodeCategory) ='TRADE_CHANNEL'
    AND DeleteFlag IS FALSE) AS g
ON
  a.TradeChannel = g.CodeValue
  AND a.SalesOrg= g.SalesOrg
LEFT JOIN (
  SELECT
    CodeDesc,
    CodeValue,
    SalesOrg,
    CountryId
  FROM
    indochina_tccc_prod.sapCodeDesc_BASE
  WHERE
    UPPER(CodeCategory) ='CUSTOMER_TYPE'
    AND DeleteFlag IS FALSE) AS h
ON
  a.customertype = h.CodeValue
  AND a.SalesOrg= h.SalesOrg
LEFT JOIN (
  SELECT
    DISTINCT RepCode AS personno,
    RepName AS firstname,
    ' ' AS lastname
  FROM
    `indochina_tccc_test.vn_secondary_hierarchy` ) AS i
ON
  i.personno = a.repid
LEFT JOIN (
  SELECT
    DISTINCT keyacc,
    id,
    codedesc
  FROM
    `indochina_tccc_test.CUSTOMERS_BASE` AS a
  INNER JOIN
    `indochina_tccc_test.sfaCodeDesc_BASE` AS b
  ON
    a.keyacc = b.codevalue
  WHERE
    codecategory = 'KeyAcc' ) AS j
ON
  a.CUSTOMER_ID = j.id'''


sql15= '''SELECT
  *
FROM (
  SELECT
    *
  FROM (
    SELECT
      order_no,
      user_id,
      customer_id,
      date,
      UOM_CODE,
      PRICE,
      Quantity_Confirmed,
      productid,
      SubGroupDesc,
      CountryID AS country
    FROM (
      SELECT
        * EXCEPT(product_id,
          PackType,
          BrandDesc)
      FROM (
        SELECT
          order_no,
          user_id,
          customer_id,
          date,
          UOM_CODE,
          PRICE,
          product_id,
          Quantity_Confirmed
        FROM (
          SELECT
            DISTINCT a.order_no,
            a.ordertype,
            a.org_id,
            SUBSTR(a.order_date,1,10) AS date,
            CAST(b.product_id AS string) AS product_id,
            a.user_id,
            a.CUSTOMER_ID,
            b.Quantity_Confirmed,
            CAST(IFNULL(b.Line_Disc_Amount, b.Line_Amount) AS float64)AS price,
            b.UOM_CODE
          FROM (
            SELECT
              DISTINCT order_no,
              ordertype,
              org_id,
              user_id,
              visit_id,
              CUSTOMER_ID,
              order_date,
              confirmed_date
            FROM
              `indochina_tccc_test.cleaned_order_headers` ) AS a
          INNER JOIN
            `indochina_tccc_test.cleaned_order_lines` AS b
          ON
            a.order_no = b.order_no)
        WHERE
          SUBSTR(date,1,4) ="2017") AS x
      LEFT JOIN (
        SELECT
          DISTINCT b.id AS productid,
          PackType,
          SubGroupDesc,
          BrandDesc
        FROM
          indochina_tccc_prod.sapProduct_BASE AS a
        INNER JOIN
          `indochina_tccc_test.PRODUCTS_BASE` AS b
        ON
          a.productid=b.code ) AS d
      ON
        LTRIM(TRIM(x.product_id),'0')= CAST(d.productid AS string)) AS g
    INNER JOIN
      `indochina_tccc_test.CUSTOMERS_BASE` AS h
    ON
      h.id=g.customer_id)
  WHERE
    country LIKE "%MM%" ) union all
SELECT
  Order_No,
  RepId,
  customerid,
  batchdate,
  UOM_CODE,
  CAST(Price AS float64),
  CAST(volume AS string),
  CAST(productid AS int64),
  subgroupdesc,
  Country
FROM (
  SELECT
    Order_No,
    RepId,
    k.customerid,
    batchdate,
    "CS" AS UOM_CODE,
    productid,
    subgroupdesc,
    Price,
    CASE
      WHEN ea2csD IS NOT NULL OR ea2csN IS NOT NULL THEN (Qty_delevered_sub*(ea2csN/ea2csD))
      ELSE (Qty_delevered_sub)
    END +
    CASE
      WHEN cs2csN IS NOT NULL OR cs2csD IS NOT NULL THEN (Qty_delevered*(cs2csN/cs2csD))
      ELSE (Qty_delevered)
    END AS volume,
    Country
  FROM (
    SELECT
      Order_No,
      RepId,
      batchdate,
      customerid,
      price,
      productid,
      SubGroupDesc,
      Qty_delevered,
      Qty_delevered_sub,
      UOM_Unit,
      UOM_Sub_Unit,
      CAST(cs2cs.ConversionBaseNominator AS float64) AS cs2csD,
      CAST(cs2cs.ConversionBaseNumerator AS float64) AS cs2csN,
      CAST(ea2cs.ConversionBaseNominator AS float64) AS ea2csD,
      CAST(ea2cs.ConversionBaseNumerator AS float64) AS ea2csN,
      CAST(cs2uc.ConversionBaseNominator AS float64) AS cs2ucD,
      CAST(cs2uc.ConversionBaseNumerator AS float64) AS cs2ucN,
      Country
    FROM (
      SELECT
        Order_No,
        RepId,
        CustomerId,
        batchdate,
        UOM_Unit,
        UOM_Sub_Unit,
        Price,
        ArticleNumber AS productid,
        Qty_Delivered_Units AS Qty_delevered,
        Qty_Delivered_Sub_Units AS Qty_delevered_sub,
        Country,
        SubGroupDesc
      FROM (
        SELECT
          * EXCEPT(ChangeDateTime,
            DeleteFlag,
            CreateDateTime)
        FROM (
          SELECT
            a.*,
            b.* EXCEPT(order_no)
          FROM (
            SELECT
              DISTINCT Order_No,
              RepId,
              CustomerId,
              batchdate
            FROM
              `indochina_tccc_prod.bosDeliveryDocumentHeader_BASE`
            WHERE
              UPPER(country) LIKE "MM" ) AS a
          LEFT JOIN
            `indochina_tccc_prod.bosDeliveryDocumentItem_BASE` AS b
          ON
            a.order_no = b.order_no) AS c
        LEFT JOIN
          `indochina_tccc_prod.sapProduct_BASE` AS sapProd
        ON
          sapProd.ProductId = c.articlenumber) ) AS x
    LEFT JOIN
      indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2cs
    ON
      x.productid = cs2cs.materialno
      AND x.UOM_Unit = cs2cs.AlternateStockKeepingUnit
    LEFT JOIN
      indochina_tccc_prod.sapMaterialConversionRate_BASE AS ea2cs
    ON
      x.productid = ea2cs.materialno
      AND x.UOM_Sub_Unit = ea2cs.AlternateStockKeepingUnit
    LEFT JOIN
      indochina_tccc_prod.sapMaterialConversionRate_BASE AS cs2uc
    ON
      x.productid = cs2uc.materialno
    WHERE
      cs2uc.AlternateStockKeepingUnit LIKE "%UC%" ) AS k)'''


sql16= '''select user_id,percentile from (SELECT
  user_id,
  ((Ci+Fi)/N)*100 AS percentile
FROM (
  SELECT
    user_id,
    (
      CASE
        WHEN incentive IS NOT NULL THEN (Row_number() OVER(PARTITION BY distributorcode ORDER BY incentive ASC))-1
        ELSE NULL END) AS Ci,
    COUNT(1)OVER(PARTITION BY distributorcode ) AS N,
    .5*(COUNT(1) OVER(PARTITION BY distributorcode, CAST(incentive AS string))) AS Fi
  FROM
    `gamification.can_nutri_volume_2018_05_31_10_32_Backup` )) where percentile is not null
'''


sql17='''SELECT
  customerid,
  subgroupDesc,
  revenue_cy_ytd
FROM (
  SELECT
    customerid,
    SubGroupDesc,
    SUM(CAST(Price AS float64)) AS revenue_cy_ytd
  FROM
    `4eManual.mm_orders_5s` 
  WHERE
    CAST(batchdate AS DATE) BETWEEN (
    SELECT
      Start_Date
    FROM
      `indochina_tccc_prod.COKE_CALENDAR`
    WHERE
      year = (
      SELECT
        year AS mn
      FROM
        indochina_tccc_prod.COKE_CALENDAR
      WHERE
        DATE_SUB(CURRENT_DATE('Asia/Saigon'),INTERVAL 1 DAY) BETWEEN start_date
        AND DATE_SUB(end_date, INTERVAL 1 day)
      LIMIT
        1)
      
    ORDER BY
      week_num
    LIMIT
      1)
    AND (DATE_SUB(CURRENT_DATE('Asia/Saigon'), INTERVAL 1 day))
    AND SubGroupDesc IS NOT NULL
  GROUP BY
    SubGroupDesc,
    customerid)

'''




sql=sql17.replace("`","")
# res = sql[165:]
res=json.dumps(parse(sql))
# res = json.loads(res)
# print (res)
def findkeys(res):
    keys_list =["left join","tablename","join","cross join","right join"]
    res_final =[]
    for keys in keys_list:
        res_final.append(find_values(keys,res))
    res_final=[x for x in res_final if x]
    return res_final

def findtablenames(res_final):
    final = []
    for keys in res_final:
        if isinstance(keys,list):
            for key in keys:
                print(type(key))
                if isinstance(key, str):
                    final.append(key)
                    print("tables : {0}".format(key))
                elif isinstance(key,dict):
                    key = json.dumps(key)
                    temp = findkeys(key)
                    for i in temp:
                        print ("table list : {0}".format(i))
                    final+=i
    return final

#
# res_final = findkeys(res)
# final=findtablenames(res_final)
#
#
# final= list(set(final))

# for keys in res_final:
#     if isinstance(keys,list) and len(keys)>0:
#         for key in keys:
#             res_final.append(findkeys(json.dumps(keys)))
#             keys.pop(key)
#             print ("list found: {0}".format(keys))
#     elif isinstance(keys,dict):
#         print ("dict Found : {0}".format(keys))
#         print ("\n\n\n")


print (res)
