mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/matome');

var matomeSchema = mongoose.Schema({
	  url:   { type: String },
	  title: { type: String },
	  res :  { type: [String]}
});
var matomeDB = mongoose.model('matomeDB', matomeSchema);

exports.matomeDB = matomeDB;
