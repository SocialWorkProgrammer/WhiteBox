package com.ssafy.whitebox.mypage.service;

import com.ssafy.whitebox.mypage.dto.UserInfoResponseParam;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MyPageService {

    private final UserRepository userRepository;

    public UserInfoResponseParam getUserInfo(UserDetails userDetails) {
        // UserDetails에서 유저 이메일을 가져와 UserRepository를 통해 유저 정보 조회
        String email = userDetails.getUsername();
        User user = userRepository.findByUserEmail(email);

        // 조회된 유저 정보를 기반으로 DTO 생성 및 반환
        return UserInfoResponseParam.builder()
                .nickname(user.userNickname())
                .email(user.userEmail())
                .createdAt(user.userDate())
                .build();
    }
}
