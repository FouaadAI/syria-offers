const fs = require('fs');

function translate(text) {
  if (!text) return text;
  let r = text;
  r = r.replace(/24 ساعة/g, '24 hours');
  r = r.replace(/مفتوح على مدار الساعة/g, 'Open 24 hours');
  r = r.replace(/من الفجر حتى العشاء/g, 'From dawn until evening');
  r = r.replace(/صباحاً/g, 'AM');
  r = r.replace(/مساءً/g, 'PM');
  r = r.replace(/مساءاً/g, 'PM');
  r = r.replace(/ظهراً/g, 'noon');
  r = r.replace(/إلى/g, 'to');
  r = r.replace(/(\d{1,2}:\d{2})\s*صباحاً/g, '$1 AM');
  r = r.replace(/(\d{1,2}:\d{2})\s*مساءً/g, '$1 PM');
  r = r.replace(/(\d{1,2}:\d{2})\s*مساءاً/g, '$1 PM');
  r = r.replace(/(\d{1,2}:\d{2})\s*ظهراً/g, '$1 noon');
  return r;
}

function translateFee(text) {
  if (!text) return text;
  return text.replace(/ل\.س/g, 'SYP');
}

// Transform tourist_data_service.dart
let content = fs.readFileSync('D:\\brain\\Documents\\uffria_app\\syria_offers_app\\lib\\services\\tourist_data_service.dart', 'utf8');
let lines = content.split('\n');
let newLines = [];
for (let line of lines) {
  newLines.push(line);
  let m = line.match(/openingHours: '([^']+)',/);
  if (m) {
    let val = m[1];
    let tr = translate(val);
    let indent = line.substring(0, line.length - line.trimStart().length);
    newLines.push(indent + "openingHoursEn: '" + tr + "',");
  }
}
fs.writeFileSync('D:\\brain\\Documents\\uffria_app\\syria_offers_app\\lib\\services\\tourist_data_service.dart', newLines.join('\n'), 'utf8');
console.log('Done tourist_data_service.dart');

// Transform cultural_data_service.dart
content = fs.readFileSync('D:\\brain\\Documents\\uffria_app\\syria_offers_app\\lib\\services\\cultural_data_service.dart', 'utf8');
lines = content.split('\n');
newLines = [];
for (let line of lines) {
  newLines.push(line);
  let m = line.match(/openingHours: '([^']+)',/);
  if (m) {
    let val = m[1];
    let tr = translate(val);
    let indent = line.substring(0, line.length - line.trimStart().length);
    newLines.push(indent + "openingHoursEn: '" + tr + "',");
  }
  let m2 = line.match(/entryFee: '([^']+)',/);
  if (m2) {
    let val = m2[1];
    let tr = translateFee(val);
    let indent = line.substring(0, line.length - line.trimStart().length);
    newLines.push(indent + "entryFeeEn: '" + tr + "',");
  }
}
fs.writeFileSync('D:\\brain\\Documents\\uffria_app\\syria_offers_app\\lib\\services\\cultural_data_service.dart', newLines.join('\n'), 'utf8');
console.log('Done cultural_data_service.dart');
