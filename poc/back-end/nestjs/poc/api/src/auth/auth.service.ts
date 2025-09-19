import {
  Injectable,
  UnauthorizedException,
  BadRequestException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import { compareSync } from 'bcrypt';
import { User } from '../users/user.entity';
import { Role } from '../common/enum/role.enum'

@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async register(
    email: string,
    username: string,
    password: string,
    role : Role,
  ) {
    const user = await this.usersService.findByEmail(email);
    if (user) throw new UnauthorizedException('User already exist');
    return this.usersService.create(email, username, password, role);
  }

  async login(email: string, password: string) {
    const user = await this.usersService.findByEmail(email);
    if (!user) throw new UnauthorizedException('Invalid credentials');

    const isMatch: boolean = compareSync(password, user.password);
    if (!isMatch) throw new UnauthorizedException('Invalid credentials');

    const payload = { sub: user.id, email: user.email, role: user.role };
    return { access_token: this.jwtService.sign(payload) };
  }

  async validateUser(email: string, password: string): Promise<User> {
    const user: User | null = await this.usersService.findByEmail(email);
    if (!user) throw new BadRequestException('User not found');
    const isMatch: boolean = compareSync(password, user.password);
    if (!isMatch) throw new BadRequestException('Password does not match');
    return user;
  }
}
