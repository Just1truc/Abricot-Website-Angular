const tarfs = require('tar-fs');
const fs = require('fs');

exports.untarFile = (filepath, newpath) => {
    fs.createReadStream(filepath).pipe(tarfs.extract(newpath));
}
