const express = require('express')
const formidable = require('formidable')
const app = express()
const port =  process.env.PORT || 3000
const path = require('path')
const fs = require('fs')

const isFileValid = (file) => {
    const type = file.type.split("/").pop();
    const validTypes = ["jpg", "jpeg", "png", "pdf"];
    if (validTypes.indexOf(type) === -1) {
      return false;
    }
    return true;
  };

app.use('/', express.static(path.join(__dirname, 'public')))

app.post('/checks', function (req, res){
    const form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
 
        let oldPath = files.profilePic.filepath;
        let newPath = path.join(__dirname, 'uploads')
            + '/' + files.profilePic.name
        let rawData = fs.readFileSync(oldPath)
 
        fs.writeFile(newPath, rawData, function (err) {
            if (err) console.log(err)
            return res.send("Successfully uploaded -> ", newPath)
        })
    })
});

app.listen(port, () => {
  console.log(`Example app listening on :  http://localhost:${port}`)
})