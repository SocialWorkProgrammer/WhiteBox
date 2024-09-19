package com.ssafy.whitebox.auth.controller;

import com.ssafy.whitebox.auth.dto.LoginRequest;
import com.ssafy.whitebox.auth.util.JWTUtil;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.service.CustomUserDetailService;
import com.ssafy.whitebox.user.service.UserService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@Tag(name="Login", description = "로그인 관련 API 명세")
@RestController
@RequestMapping("/api/v1/users")
public class LoginController {

    private final AuthenticationManager authenticationManager;
    private final JWTUtil jwtUtil;
    private final UserService userService;

    public LoginController(AuthenticationManager authenticationManager, JWTUtil jwtUtil, UserService userService) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
        this.userService = userService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest loginRequest) {
        String username = loginRequest.getUser_email();
        try {
            UsernamePasswordAuthenticationToken authenticationToken =
                    new UsernamePasswordAuthenticationToken(loginRequest.getUser_email(), loginRequest.getUser_password());

            Authentication authentication = authenticationManager.authenticate(authenticationToken);

            // JWT 토큰 생성
            String token = jwtUtil.createJwt(authentication.getName(), "USER", 7200000L);
            User user = userService.getUserByEmail(username);
            Map<String, Object> response = new HashMap<>();
            response.put("token", token);
            response.put("message", "로그인 성공");
            response.put("userNickname", user.userNickname());
            response.put("userType", user.userType().getValue());
            response.put("registrationDate", user.userDate());
            System.out.println(response);
            return ResponseEntity.ok(response);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
        }
    }
}
