<template>
	<view class="content">
		<view class="page">
			<view class="result-list">
				<view>
					<text>当前位置地址信息：</text>
					<view class="address-name" v-show="addressName">{{addressName.province}}{{addressName.district}}</view>
					<view class="address-name" v-show="addressName">{{allAddress}}</view>
				</view>
				<view>
					<text>当前位置天气简况：</text>
					<rich-text v-if="weather.hasData" :nodes="weather.data"></rich-text>
				</view>
			</view>
			<view class="btn-list">
				<button type="primary" @tap="getRegeo">获取当前地址信息</button>
				<button type="primary" @tap="getWeather">获取实时天气数据</button>
			</view>
		</view>
	</view>
</template>
<script>
	import amap from '../../../common/amap-wx.js';
	export default {
		data() {
			return {
				hasLocation: false,
				location: {},
				amapPlugin: null,
				key: '044ac57e5a765e13efbe28f63077ec15',
				addressName: '',
				weather: {
					hasData: false,
					data: []
				},
				allAddress: ''
			}
		},
		onLoad() {
			this.amapPlugin = new amap.AMapWX({
				key: this.key
			});
		},
		methods: {
			getRegeo() {
				uni.showLoading({
					title: '定位中'
				});
				this.amapPlugin.getRegeo({
					success: (data) => {
						console.log(JSON.stringify(data))
						this.addressName = data[0].regeocodeData.addressComponent;
						this.allAddress = data[0].regeocodeData.formatted_address;
						console.log(this.addressName.province)
						console.log(this.addressName.district)
						uni.hideLoading();
					}
				});
			},
			getWeather() {
				uni.showLoading({
					title: '获取信息中'
				});
				this.amapPlugin.getWeather({
					success: (data) => {
						console.log(data);
						for (const key in data) {
							console.log(key);
							if (key !== 'liveData') {
								this.weather.data.push({
									name: 'div',
									children: [{
										type: 'text',
										text: data[key].text + '：' + data[key].data
									}]
								});
							}
						}
						uni.hideLoading();
						this.weather.hasData = true;
					}
				});
			}
		}
	}
</script>

<style>
	view {
		display: block;
	}
	.content{
		width: 660upx;
		margin: 0 auto;
	}
	.page {
		display: flex;
		flex: 1;
		justify-content: center;
		flex-direction: column;
		width: 100%;
		text-align: center;
	}
	.result-list{
		padding: 40upx;
	}
	.result-list view{
		padding: 10upx 0;
	}
	.result-list view rich-text{
		font-size: 28upx;
	}

	.btn-list button {
		width: 100%;
		height: 80upx;
		margin: 0 auto 40upx;
		text-align: center;
		line-height: 80upx;
		background: #918984;
		color: #FFFFFF;
		border-radius: 40upx;
	}
	.address-name{
		font-size: 28upx;
	}
</style>
