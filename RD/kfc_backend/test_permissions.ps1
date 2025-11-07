# 简单的权限测试脚本
Write-Host "===== 测试管理员权限接口 ====="

# 1. 普通用户登录
Write-Host "\n1. 测试普通用户登录..."
$loginBody = @{"username"="frontend";"password"="test123456"} | ConvertTo-Json
$loginResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/users/login/" -Method POST -ContentType "application/json" -Body $loginBody -UseBasicParsing
Write-Host "登录状态码: $($loginResponse.StatusCode)"

# 2. 获取token并测试访问管理员接口
if ($loginResponse.StatusCode -eq 200) {
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $token = $loginData.token
    Write-Host "获取到token: $token"
    
    Write-Host "\n2. 测试普通用户访问管理员接口..."
    try {
        $adminResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/users/" -Method GET -Headers @{"Authorization"="Token $token"} -UseBasicParsing
        Write-Host "访问状态码: $($adminResponse.StatusCode)"
        Write-Host "响应内容: $($adminResponse.Content)"
    } catch {
        Write-Host "访问被拒绝，错误信息: $($_.Exception.Response.StatusCode)"
        Write-Host "详细信息: $($_.ErrorDetails.Message)"
    }
}

# 3. 尝试管理员登录
Write-Host "\n3. 尝试管理员账号登录..."
try {
    $adminLoginBody = @{"username"="admin";"password"="admin123456"} | ConvertTo-Json
    $adminLoginResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/users/login/" -Method POST -ContentType "application/json" -Body $adminLoginBody -UseBasicParsing
    Write-Host "管理员登录状态码: $($adminLoginResponse.StatusCode)"
} catch {
    Write-Host "管理员登录失败: $($_.Exception.Response.StatusCode)"
    Write-Host "错误信息: $($_.ErrorDetails.Message)"
}

Write-Host "\n===== 测试完成 ====="