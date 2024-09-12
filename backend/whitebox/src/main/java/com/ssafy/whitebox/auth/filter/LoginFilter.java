package com.ssafy.whitebox.auth.filter;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ssafy.whitebox.auth.dto.LoginRequest;
import com.ssafy.whitebox.auth.util.JWTUtil;
import com.ssafy.whitebox.user.dto.CustomUserDetails;
import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import java.io.IOException;
import java.util.Collection;
import java.util.Iterator;

public class LoginFilter extends UsernamePasswordAuthenticationFilter {

    private final AuthenticationManager authenticationManager;
    private final JWTUtil jwtUtil;

    public LoginFilter(AuthenticationManager authenticationManager, JWTUtil jwtUtil) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
        // login 엔드 포인트 변경
        setFilterProcessesUrl("/api/v1/users/login");
    }

    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException{

        ObjectMapper objectMapper = new ObjectMapper();
        LoginRequest loginRequest = null;  // RequestBody에서 데이터 읽기
        try {
            loginRequest = objectMapper.readValue(request.getInputStream(), LoginRequest.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String email = loginRequest.getUser_email();
        String password = loginRequest.getUser_password();

        System.out.println("Attempting authentication for user: " + email);
        if (email == null || email.isEmpty()) {
            throw new UsernameNotFoundException("Email not provided");
        }
        UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(email, password, null);

        return authenticationManager.authenticate(authToken);
    }


    // JWT 토큰 발급
    @Override
    protected void successfulAuthentication(HttpServletRequest request, HttpServletResponse response, FilterChain chain, Authentication authentication) {
        CustomUserDetails customUserDetails =  (CustomUserDetails) authentication.getPrincipal();
        String username = customUserDetails.getUsername();

        // 역활 뽑아오기
        Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();
        Iterator<? extends  GrantedAuthority> iterator  = authorities.iterator();
        GrantedAuthority auth =  iterator.next();

        String role = auth.getAuthority();
        String token = jwtUtil.createJwt(username, role, 60*60*10L);

        // rfc - 7235 정의, header에 Authorization를 붙인다.
        response.addHeader("Authorization", "Bearer " + token);
    }

    @Override
    protected void unsuccessfulAuthentication(HttpServletRequest request, HttpServletResponse response, AuthenticationException failed) {
        response.setStatus(401);
    }
}
