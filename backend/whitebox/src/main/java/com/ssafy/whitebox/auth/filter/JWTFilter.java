package com.ssafy.whitebox.auth.filter;

import com.ssafy.whitebox.auth.util.JWTUtil;
import com.ssafy.whitebox.user.dto.CustomUserDetails;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.util.UserType;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

public class JWTFilter extends OncePerRequestFilter {

    private final JWTUtil jwtUtil;

    public JWTFilter(JWTUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        String authorization = request.getHeader("Authorization");

        if (authorization == null || !authorization.startsWith("Bearer ")) {
            System.out.println("token null");
            filterChain.doFilter(request, response);
            return;
        }

        System.out.println("authorization now");
        // 순수 token 획득
        String token = authorization.split(" ")[1];
        
        // 시간이 소멸 시
        if (jwtUtil.isExpired(token)) {

            System.out.println("token expired");
            filterChain.doFilter(request, response);
            return;
        }

        String username = jwtUtil.getUsername(token);
        String role = jwtUtil.getRole(token);

        User user = new User();
        user.userEmail(username);
        user.userPassword("temp");
        user.userNickname("temp_user");
        user.userType(UserType.valueOf(role));

        CustomUserDetails customUserDetails = new CustomUserDetails(user);
        Authentication authToken = new UsernamePasswordAuthenticationToken(customUserDetails, null, customUserDetails.getAuthorities());
        // 세션에 사용자 등록하기
        SecurityContextHolder.getContext().setAuthentication(authToken);

        // 그다음 필터에게 request, response 넘겨주기
        filterChain.doFilter(request, response);

    }
}
