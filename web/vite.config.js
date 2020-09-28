export default {
    proxy:{
        '/api':{
            target:"http://localhost:10279/"
        }
    },
    outDir:"../server/dist",
    assetsDir:"static"
}