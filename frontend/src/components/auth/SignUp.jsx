import "../../styles/auth/sign-up.css";
import { useNavigate } from 'react-router-dom';
import { useState } from "react";
import useAuthStore from "../../store/useAuthStore";
import { Helmet } from 'react-helmet';

function SignUp() {
    const navigate = useNavigate();
    const { checkEmail, checkNickname, signUp, login} = useAuthStore();

    const [user, setUser] = useState({
        id: "",
        nickname: "",
        password: "",
        passwordConfirm: "",
    });

    const handleOnChange = (event) => {
        const { name, value } = event.target;
        setUser({
            ...user, [name]: value,
        });
    };

    const validatePassword = (password) => {
        // 비밀번호는 최소 8자 이상, 숫자와 문자를 포함해야 함
        const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        return regex.test(password);
    };

    const handleOnSubmit = async (event) => {
        event.preventDefault();

        if (!validatePassword(user.password)) {
            alert("비밀번호는 최소 8자 이상이며, 숫자와 문자를 포함해야 합니다.");
            return;
        }

        if (user.password !== user.passwordConfirm) {
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }

        try {
            const emailCheck = await checkEmail({id: user.id});
            if (!emailCheck.isSuccess) {
                alert("이미 가입한 이메일입니다.");
                return;
            }

            const nicknameCheck = await checkNickname({nickname: user.nickname});
            if (!nicknameCheck.isSuccess) {
                alert("이미 사용 중인 닉네임입니다.");
                return;
            } 

            signUp(user);
            // 메인 페이지로 이동
            navigate(`/auth/profile/${user.nickname}`);
        } catch (error) {
            console.error("회원가입 과정 중 오류 발생:", error);
            alert("회원가입 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        }
    };

    return (
        <div>
            <Helmet>
                <title>White Box | 회원가입</title>
            </Helmet>
            <div className="title">회원가입</div>
            <div className="description">White Box의 회원이 되시면 다양한 서비스를 이용하실 수 있습니다.</div>
            <div className="signup-modal">
                <form onSubmit={handleOnSubmit}>
                    <div className="form-group">
                        <label htmlFor="id">이메일</label>
                        <input type="email" id="id" name="id" value={user.id} onChange={handleOnChange} required/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="nickname">닉네임</label>
                        <input type="text" id="nickname" name="nickname" value={user.nickname} onChange={handleOnChange} required/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">비밀번호</label>
                        <input type="password" id="password" name="password" value={user.password} onChange={handleOnChange} required/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="passwordConfirm">비밀번호 확인</label>
                        <input type="password" id="passwordConfirm" name="passwordConfirm" value={user.passwordConfirm} onChange={handleOnChange} required/>
                    </div>

                    <button className="button" type="submit">회원가입</button>
                </form>
            </div>
        </div>
    );
};

export default SignUp;