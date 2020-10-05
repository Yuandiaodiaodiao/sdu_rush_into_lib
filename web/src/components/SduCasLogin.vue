<!--
使用方法
<SduCasLogin v-model:islogin="islogin"></SduCasLogin>
-->


<style scoped>
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

    .aspin {
        margin-top: 20px;
    }
</style>
<template>


    <a-spin class="aspin" v-if="loginLoading" tip="登陆中..."/>
    <div v-else>
        <div v-if="!islogin" class="inputBox">
            <input placeholder="学号" v-model="userid"/>
            <input placeholder="密码" type="password" v-model="passwd"/>
            <a-button @click="login()">记住并登录</a-button>
        </div>
        <div class="inputBox" v-else>
            <a-button @click="logout()">退出登录</a-button>
        </div>
    </div>
</template>

<script>
    import {getCurrentInstance, onBeforeMount, ref, toRefs, watchEffect, inject} from "vue";
    import axios from "axios"
    import {strEnc, strDec} from "../util/des.js"

    export default {
        name: "SduCasLogin",
        props: {
            islogin: {
                type: Boolean,
                default: false
            }
        },
        setup(props) {
            const {islogin} = toRefs(props)
            const {ctx} = getCurrentInstance()
            const message = inject("message")


            const changeLoginState = (value) => {

                console.log(`emit update:islogin ${value}`)
                // ctx.$emit("update:islogin", value)
                //vite打包暂时有bug 直接用_.代替$
                ctx._.emit("update:islogin", value)
            }

            watchEffect(() => {
                console.log("sducaslogin.vue:" + islogin.value)
            })
            const userid = ref("")
            const passwd = ref("")
            const loginLoading = ref(false)
            const login = async () => {
                try {
                    loginLoading.value = true
                    const lt = (await axios.get("/api/lt")).data
                    //后端拉网页拿到lt
                    const rsa = strEnc(userid.value + passwd.value + lt, "1", "2", "3")
                    //des加密
                    const res = await axios.post("/api/lt",
                        {rsa, lt, ul: userid.value.length, pl: passwd.value.length})
                    loginLoading.value = false
                    if (res.data === "success") {
                        message.success("登录成功", 1)

                        localStorage.setItem('userid', userid.value)
                        //密码也加密一下存进去
                        const passwordEncode = strEnc(userid.value + passwd.value, userid.value, userid.value, userid.value)
                        localStorage.setItem('passwordEncode', passwordEncode)
                        changeLoginState(true)
                    } else {
                        changeLoginState(false)
                        message.error("登录失败", 1)
                    }

                } catch (e) {
                    loginLoading.value = false
                    message.error(`登录失败${e}`, 1)
                }

            }
            onBeforeMount(async () => {
                const useridt = localStorage.getItem('userid')
                if (useridt && useridt.length > 5) {
                    //不会有人学号少于5位数吧
                    userid.value = localStorage.getItem('userid')
                    const passwordEncode = localStorage.getItem('passwordEncode')
                    const password = strDec(passwordEncode, userid.value, userid.value, userid.value)
                    passwd.value = password.split(userid.value)[1]
                    await login()
                }
            })


            const logout = () => {
                localStorage.removeItem('userid')
                localStorage.removeItem('passwd')
                localStorage.removeItem('rsa')
                changeLoginState(false)
            }

            return {
                login, userid, passwd, logout, loginLoading
            }
        }
    }
</script>
