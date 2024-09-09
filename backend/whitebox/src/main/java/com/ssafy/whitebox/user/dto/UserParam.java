package com.ssafy.whitebox.user.dto;
import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.user.util.UserType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Setter;

// Getter, Setter, RequiredArgsConstructor, ToString, EqualsAndHashCode
@Data
@Setter(AccessLevel.NONE)
public class UserParam {

    @Schema(description = "사용자 이메일")
    String userEmail;

    @Setter
    @Schema(description = "사용자 비밀번호")
    String userPassword;

    @Schema(description = "사용자 닉네임")
    String userNickname;

    @Schema(description = "사용자 타입")
    @Setter
    UserType userType;


    // 정적 Factory method
    public static UserParam from(User user) {
        UserParam userParam = new UserParam();
        userParam.userEmail = user.getUserEmail();          // User의 이메일 값 설정
        userParam.userPassword = user.getUserPassword();    // User의 비밀번호 값 설정
        userParam.userNickname = user.getUserNickname();    // User의 닉네임 값 설정
        userParam.userType = user.getUserType();            // User의 타입 설정

        return userParam;
    }


}

