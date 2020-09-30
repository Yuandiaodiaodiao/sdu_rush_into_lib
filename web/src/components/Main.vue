<style scoped>
    .timebox {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50px;
    }

    .timebox > div {
        margin: auto 5px;
    }

    .inputBox {

        display: flex;
        flex-direction: column;
        margin: 20px;
        justify-content: center;
        align-items: center;
    }

    .inputBox > * {
        width: 70vw;
        margin: 5px;
    }
</style>

<template>
    <div v-if="!islogin" class="inputBox">
        <input placeholder="学号" v-model="userid"/>
        <input placeholder="密码" type="password" v-model="passwd"/>
        <a-button @click="login()">记住并登录</a-button>
    </div>
    <div class="inputBox" v-else>
        <a-button @click="logout()">退出登录</a-button>
    </div>
    <div class="timebox" v-for="(item,index) in timeInfo" :key="index">
        <div>{{item["timeStart"]}}</div>
        <div>~</div>
        <div>{{item["timeEnd"]}}</div>
        <div>
            <a-button type="primary" @click="rush(item)">🐍 冲！</a-button>
        </div>
        <div>
            <a-button type="danger" @click="quit(item)">爬!</a-button>
        </div>
    </div>
    <a-button @click="getOrder()">查看已预订</a-button>

</template>

<script>
    import {ref, reactive, onBeforeMount, getCurrentInstance} from "vue"
    import axios from "axios"
    import {strEnc} from "../util/des.js"

    export default {
        name: "Main",

        setup() {
            const {ctx} = getCurrentInstance()
            const timeInfo = ref([])
            const userid = ref("")
            const passwd = ref("")
            const islogin = ref(false)
            const login = async () => {
                try{
                    const lt = (await axios.get("/api/lt")).data
                    const rsa = strEnc(userid.value + passwd.value + lt, "1", "2", "3")
                    const res = await axios.post("/api/lt",
                        {rsa, lt, ul: userid.value.length, pl: passwd.value.length})
                    console.log(res.data)
                    if(res.data==="success"){

                    }else{
                        alert("登录失败")
                        return
                    }
                    console.log("存储" + userid.value)
                    localStorage.setItem('userid', userid.value)
                    localStorage.setItem('passwd', passwd.value)
                    islogin.value = true
                }catch(e){
                    alert("登录失败")
                    
                }

            }
            onBeforeMount(async () => {
                const res = await axios.get("/api/list")
                timeInfo.value = res.data

                const useridt = localStorage.getItem('userid')
                if (useridt && useridt.length > 5) {
                    islogin.value = true
                    userid.value = localStorage.getItem('userid')
                    passwd.value = localStorage.getItem('passwd')
                    await login()
                }
            })


            const logout = () => {
                localStorage.removeItem('userid')
                localStorage.removeItem('passwd')
                islogin.value = false

            }
            const rush = async (item) => {
                const res = await axios.post("api", {op: "rush", ...item})
                console.log(res.data)

                if(res.data.status===1){
                    alert("预约成功")
                }else{
                    if(res.data.msg==="用户未登录"){
                        alert("正在重新登录")
                        await login()
                        await rush(item)
                    }else{
                        alert("申请失败")
                    }
                }
            }
            const quit=async(item)=>{
                const res = await axios.post("api", {op: "quit", ...item})
                console.log(res.data)
                if(res.data.status===1){
                    alert("爬爬爬我最会爬了")
                }else{
                    alert("爬都能爬歪来👎")
                }
            }
            const getOrder=async ()=>{
                const res = await axios.post("api", {op: "list"})
                console.log(res)

            }
            return {
                timeInfo, rush, login, islogin, userid, passwd, logout,getOrder,quit
            }
        }
    }
</script>
