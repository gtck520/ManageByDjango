exports.install = function (Vue, options) {
	// 参数： url:请求地址  param：请求参数  way：请求方式 res：回调函数
   Vue.prototype.urlRequest = function(param) {
		let httpurl='http://127.0.0.1:8000/'
		// let deviceId = ''
 
// 		uni.getStorage({
// 			key: 'deviceIds',
// 			success: function(res) {
// 				deviceId = res.data;
// 			}
// 		})
//  
// 		let baseParam = {
// 			deviceId: deviceId,
// 			os: "ios",
// 			version: "",
// 			appName: "wsj",
// 		}
 
		let token = uni.getStorageSync('token'); 
		uni.request({
			url: httpurl+param.url,
			// data: JSON.stringify(Object.assign(param.data, baseParam)),
			data:param.data,
			header: {
				'JWT': token,
				'Accept': 'application/json',
				'Content-Type': 'application/json', //自定义请求头信息
			},
			method: param.method,
			success: (data) => {
				// console.log("网络请求返回值:"+ JSON.stringify(data))
				param.success(data)
			},
			fail: (data) => {
				param.fail(data)
			},
			complete: (data) => {
				param.complete(data)
			}
		});
 
 
	};
	//验证token提取用户信息
	Vue.prototype.getGlobalUser = function(callback) {
		var token = uni.getStorageSync('token');
		if (token != null && token != "" && token != undefined) {
			this.urlRequest({
				url: 'v1/userinfo/',
				data: {},
				method: 'GET',
				success: res => {
					if (res.statusCode == 200) {
						uni.setStorageSync('userinfo',res.data);
						callback(res.data);
					}else{
						callback(null);
					}
				},
				fail: () => {},
				complete: () => {}
			});
		} else {
			callback(null);
		}
	};
};