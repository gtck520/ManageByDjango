<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content">{{fullname}}</block>
			</cu-custom>
		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				<text class="cuIcon-title text-blue"></text>{{ChapterSN}}
			</view>
		</view>
		<view class="padding bg-white">
			<view class="text-left padding" v-for="(item,index) in contentlist" :key="index">
				<view class='cu-tag round'>{{item.VerseSN}}</view>
				{{item.Lection}}
			</view>
		</view>
	</view>
	
</template>

<script>
	export default {
		data() {
			return {
				contentlist:{},
				fullname:'',
				ChapterSN:''
			}
		},
		onLoad(o) {
			this.getcontents(o.booksn,o.chaptersn);
		},
		methods: {
			getcontents(booksn,chaptersn){
				// 获取节列表
				uni.request({
				url: this.ApiHost+'v1/contents/'+booksn+'/'+chaptersn+'/',
				data: {},
				method: 'GET',
				}) .then(data => {
					var [error, res]  = data;
					this.contentlist = res.data;
					this.ChapterSN=res.data[0]['ChapterSN']
					this.fullname=res.data[0]['VolumeSN'].FullName;
					console.log(this.contentlist);
				});
			}
		}
	}
</script>

<style>

</style>
