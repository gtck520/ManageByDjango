<template>
	<view class="content">
		<view v-if="!changeSuccess">
			<view class="uni-form-item uni-column">
				<input type="tel" class="uni-input" name="" placeholder="请输入手机号" />
			</view>
			<view class="uni-form-item uni-column column-with-btn">
				<input type="text" class="uni-input" name="" placeholder="请输入图片验证码" v-model="captchaImg" />
				<image src="../../static/login-registration/captcha.jpg" mode="" class="img-captcha"></image>
			</view>
			<view class="uni-form-item uni-column column-with-btn">
				<input type="number" class="uni-input" name="" placeholder="请输入验证码" />
				<button :class="{active : !disableCodeBtn}" :disabled="disableCodeBtn" @tap="sendCode">{{codeBtn.text}}</button>
			</view>
			<view class="uni-form-item uni-column">
				<input type="password" class="uni-input" name="" placeholder="请输入新密码" />
			</view>
			<button type="primary" @tap="changeSuccess = !changeSuccess">提交</button>
		</view>
		<view v-if="changeSuccess">
			<view class="text-reset">重置成功，新密码已生效！</view>
			<button type="primary" @tap="gotoLogin">立即登陆</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				captchaImg: '',
				seconds: 10,
				codeBtn: {
					text: '获取验证码',
					waitingCode: false,
					count: this.seconds
				},
				changeSuccess: false
			}
		},
		onLoad() {

		},
		methods: {
			sendCode: function () {
				this.codeBtn.waitingCode = true;
				this.codeBtn.count = this.seconds;
				this.codeBtn.text = this.codeBtn.count + 's';
				
				let countdown = setInterval( () => {
					this.codeBtn.count--;
					this.codeBtn.text = this.codeBtn.count + 's';
					if( this.codeBtn.count < 0 ){
						clearInterval(countdown);
						this.codeBtn.text = '重新发送';
						this.codeBtn.waitingCode = false;
					}
				},1000);
			},
			gotoLogin: function () {
				uni.navigateTo({
					url: 'login'
				})
			}
		},
		computed: {
			disableCodeBtn: function (){
				return this.codeBtn.waitingCode || this.captchaImg.length < 4;
			} 
		}
	}
</script>

<style lang="scss" scoped>
	$color-primary: #b49950;
	.content{
		padding: 100upx;
	}
	.uni-form-item{
		margin-bottom: 40upx;
		padding: 0;
		border-bottom: 1px solid #e3e3e3;
		.uni-input{
			font-size: 30upx;
			padding: 7px 0;
		}
	}
	.column-with-btn{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		button{
			font-size: 24upx;
			margin: 0;
			width: 180upx;
			text-align: center;
			&:after{
				border: none
			}
			&.active{
				background-color: $color-primary;
				color: $uni-text-color-inverse;
			}
		}
	}
	.img-captcha{
		width: 150upx;
		height: 60upx;
	}
	button[type="primary"]{
		background-color: $color-primary;
		border-radius: 0;
		font-size: 34upx;
		margin-top: 60upx;
	}
	.text-reset{
		text-align: center;
		margin-bottom: 100upx;
		font-size: 36upx;
	}
</style>
