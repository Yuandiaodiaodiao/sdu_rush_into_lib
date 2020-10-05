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


</style>

<template>
    <SduCasLogin v-model:islogin="islogin"></SduCasLogin>
    <div v-show="islogin" class="timebox" v-for="(item,index) in timeInfo" :key="index">
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
    import {ref, reactive, onBeforeMount, getCurrentInstance, watchEffect, inject} from "vue"
    import axios from "axios"
    import SduCasLogin from "./SduCasLogin.vue";
    export default {
        name: "Main",
        components:{
            SduCasLogin
        },
        setup() {
            const {ctx} = getCurrentInstance()
            const timeInfo = ref([])
            const islogin=ref(false)
            const message=inject("message")

            watchEffect(()=>{
                console.log("Main.vue: "+islogin.value)
            })
            onBeforeMount(async () => {
                const res = await axios.get("/api/list")
                timeInfo.value = res.data

            })


            const rush = async (item) => {
                const res = await axios.post("api", {op: "rush", ...item})
                console.log(res.data)

                if(res.data.status===1){
                    message.success("预约成功")
                }else{
                    if(res.data.msg==="用户未登录"){
                        message.warning("用户未登录")
                        islogin.value=false
                    }else{
                        message.error(`申请失败 ${res.data.msg}`)
                    }
                }
            }
            const quit=async(item)=>{
                const res = await axios.post("api", {op: "quit", ...item})
                console.log(res.data)
                if(res.data.status===1){
                    message.success("爬爬爬我最会爬了")
                }else{
                    message.error("爬都能爬歪来👎")
                }
            }
            const getOrder=async ()=>{
                const res = await axios.post("api", {op: "list"})
                console.log(res)

            }
            return {
                timeInfo, rush, getOrder,quit,islogin
            }
        }
    }
</script>
