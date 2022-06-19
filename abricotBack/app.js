const express = require('express');
const dotenv = require('dotenv');
const multer = require('multer');
const upload = multer({dest: 'uploads/'});
var { PythonShell } = require('python-shell');
const fs = require('fs');
const cors = require('cors');
const app = express();
const {
    untarFile
} = require('./unpack');
const serverless = require('serverless-http');
const router = express.Router();
var type = upload.single('file');

dotenv.config();

app.use(express.json());

app.use(cors());

const getRandomName = () => {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}


router.post('/check-norme', type, (req, res, next) => {
    var randomName = getRandomName();
    var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: ['--dir', 'uploads']
    };
    untarFile(req.file.path, './uploads/' + randomName);
    PythonShell.run('brico.py', options, (err, results) => {
        if (err) throw err;
        fs.rmdir('./uploads/' + randomName, {recursive: true}, (err) => {});
        fs.rmdir(req.file.path, {recursive: true}, (err) => {});
        res.send(results);
    });
});

//app.listen(process.env.PORT || 3000, () => {
//    console.log(`Server running boi on port ${process.env.PORT || 3000}`);
//})

app.use('/.netlify/functions/api', router);

module.exports.handler = serverless(app);
