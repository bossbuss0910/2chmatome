var express = require('express');
var router = express.Router();
var client = require('cheerio-httpcli');


//POST処理
var bodyParser = require('body-parser');
router.use(bodyParser());     

//データベース用意
var model = require('../models/matomedb.js');
var matomeDB  = model.matomeDB;
var outDB = model.outDB;
var Url=null;
var title = null

/* GET users listing. */
router.post('/input', function(req, respon, next) {
	Url=req.body.url;
	client.fetch(req.body.url,{},function (err, $, res) {
		var new2ch = new matomeDB();
		new2ch.url =req.body.url;
		new2ch.title=$('title').text();
		title = new2ch.title
	//		$('div').each(function (idx) {
			reslist=$('div').find('dt').slice(0, 1).text().split('\n');
	//		reslist.push($('dt').text());
	//		  });
		  new2ch.res=reslist;
		  new2ch.save();
		  respon.redirect('/matome/out');
		});
});


router.get('/out',function(req, res, next){
	outDB.findOne({url:Url},function(err,memo){
	res.render('outputmatome',{title:memo.title,output:memo.res});
	outDB.remove({ url: Url }, function(err, result){
		if (err) {
			res.send({'error': 'An error has occurred - ' + err});
			} else {
				console.log('Success: ' + result + ' document(s) deleted');
				}
				});
	});
});



module.exports = router;
