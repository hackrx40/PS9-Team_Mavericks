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

app.post('/checks', async (req, res, next) => {
    const form = new formidable.IncomingForm();
    const uploadFolder = path.join(__dirname, "public", "files");
    form.multiples = true;
    form.parse(req, async (err, fields, files) => {
        console.log(fields);
        console.log(files);
        if (err) {
          console.log("Error parsing the files");
          return res.status(400).json({
            status: "Fail",
            message: "There was an error parsing the files",
            error: err,
          });
        }
      });
      if (!files.myFile.length) {
        //Single file
      
        const file = files.myFile;
      
        // checks if the file is valid
        const isValid = isFileValid(file);
      
        // creates a valid name by removing spaces
        const fileName = encodeURIComponent(file.name.replace(/\s/g, "-"));
      
        if (!isValid) {
          // throes error if file isn't valid
          return res.status(400).json({
            status: "Fail",
            message: "The file type is not a valid type",
          });
        }
        try {
          // renames the file in the directory
          fs.renameSync(file.path, join(uploadFolder, fileName));
        } catch (error) {
          console.log(error);
        }
      
        try {
          // stores the fileName in the database
          const newFile = await File.create({
            name: `files/${fileName}`,
          });
          return res.status(200).json({
            status: "success",
            message: "File created successfully!!",
          });
        } catch (error) {
          res.json({
            error,
          });
        }
      } else {
        // TODO:Multiple files
        console.log("multiple files")
      }
});

app.listen(port, () => {
  console.log(`Example app listening on :  http://localhost:${port}`)
})